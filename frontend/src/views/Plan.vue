<template>
  <div class="min-h-screen">
    <Sidebar />
    <main class="ml-64 p-8">
      <div class="mb-8">
        <h2 class="text-2xl font-bold">规划方案</h2>
        <p class="text-white/60 mt-1">生成短期、中期、长期职业规划，规划您的人生路线</p>
      </div>
      
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div class="lg:col-span-1">
          <div class="bg-white/5 backdrop-blur-xl rounded-xl p-6 border border-white/10">
            <h3 class="text-lg font-semibold mb-4">生成规划</h3>
            <div v-if="!diagnosis" class="text-center text-white/40 py-8">
              <p>请先进行职业诊断</p>
              <el-button type="primary" size="small" @click="$router.push('/diagnosis')" class="mt-4">去诊断</el-button>
            </div>
            <div v-else>
              <el-form :model="form" ref="formRef" class="space-y-4">
                <el-form-item label="规划类型">
                  <el-select v-model="form.plan_type" placeholder="请选择">
                    <el-option label="短期规划（1年）" value="short_term"></el-option>
                    <el-option label="中期规划（3年）" value="mid_term"></el-option>
                    <el-option label="长期规划（5-10年）" value="long_term"></el-option>
                  </el-select>
                </el-form-item>
                <el-button 
                  type="primary" 
                  :loading="loading"
                  class="w-full"
                  @click="handleGenerate"
                >
                  📋 生成{{ planTypeName }}规划
                </el-button>
              </el-form>
            </div>
          </div>
          
          <div v-if="plans.length" class="mt-6 bg-white/5 backdrop-blur-xl rounded-xl p-6 border border-white/10">
            <h3 class="text-lg font-semibold mb-4">规划列表</h3>
            <div class="space-y-2">
              <div 
                v-for="plan in plans" 
                :key="plan.id"
                class="p-3 bg-white/5 rounded-lg cursor-pointer hover:bg-white/10 transition-colors"
                :class="{ 'bg-star-primary/20': selectedPlan?.id === plan.id }"
                @click="selectPlan(plan)"
              >
                <p class="font-medium text-sm">{{ plan.title }}</p>
                <p class="text-xs text-white/50">{{ planTypeNameMap[plan.plan_type] }}</p>
              </div>
            </div>
          </div>
        </div>
        
        <div class="lg:col-span-2">
          <div class="bg-white/5 backdrop-blur-xl rounded-xl p-6 border border-white/10">
            <div v-if="selectedPlan" class="space-y-6">
              <div class="flex items-center justify-between">
                <div>
                  <h3 class="text-lg font-semibold">{{ selectedPlan.title }}</h3>
                  <p class="text-sm text-white/50">{{ planTypeNameMap[selectedPlan.plan_type] }}</p>
                </div>
                <span class="text-sm bg-star-primary/20 text-star-cyan px-3 py-1 rounded-full">{{ selectedPlan.milestones?.length || 0 }} 个里程碑</span>
              </div>
              
              <p class="text-white/80 text-sm">{{ selectedPlan.description }}</p>
              
              <div>
                <div class="flex items-center gap-2 mb-4">
                  <h4 class="font-medium">路径选择</h4>
                  <div class="flex gap-2">
                    <el-button 
                      size="small" 
                      @click="activePath = 'recommended'"
                      :class="{ 'bg-star-primary text-white': activePath === 'recommended' }"
                    >
                      推荐路径
                    </el-button>
                    <el-button 
                      v-for="(path, index) in selectedPlan.alternative_paths" 
                      :key="index"
                      size="small"
                      @click="activePath = `alternative_${index}`"
                      :class="{ 'bg-star-primary text-white': activePath === `alternative_${index}` }"
                    >
                      备选{{ index + 1 }}
                    </el-button>
                  </div>
                </div>
                
                <div v-if="activePath === 'recommended' && selectedPlan.recommended_path" class="mb-4">
                  <p class="text-sm font-medium text-star-cyan">{{ selectedPlan.recommended_path.name }}</p>
                  <p class="text-xs text-white/60">{{ selectedPlan.recommended_path.description }}</p>
                </div>
                <div v-else-if="selectedPlan.alternative_paths?.length">
                  <template v-for="(path, index) in selectedPlan.alternative_paths" :key="index">
                    <div v-if="activePath === `alternative_${index}`" class="mb-4">
                      <p class="text-sm font-medium text-star-cyan">{{ path.name }}</p>
                      <p class="text-xs text-white/60">{{ path.description }}</p>
                    </div>
                  </template>
                </div>
              </div>
              
              <div class="relative">
                <div class="absolute left-6 top-0 bottom-0 w-0.5 bg-white/20"></div>
                
                <div class="space-y-6">
                  <div 
                    v-for="(milestone, index) in filteredMilestones" 
                    :key="index"
                    class="relative pl-16"
                  >
                    <div 
                      class="absolute left-4 w-5 h-5 rounded-full flex items-center justify-center border-2"
                      :class="getMilestoneClass(milestone)"
                    >
                      <div class="w-2 h-2 rounded-full bg-white"></div>
                    </div>
                    
                    <div class="p-4 bg-white/5 rounded-xl hover:bg-white/10 transition-colors">
                      <div class="flex items-start justify-between">
                        <div>
                          <div class="flex items-center gap-2">
                            <span class="font-medium">{{ milestone.title }}</span>
                            <span class="text-xs px-2 py-0.5 rounded-full" :class="getProbabilityClass(milestone.probability)">{{ Math.round(milestone.probability * 100) }}%</span>
                          </div>
                          <p class="text-xs text-white/50 mt-1">{{ milestone.target_date }}</p>
                          <div v-if="milestone.metrics?.target_role" class="text-xs text-white/60 mt-1">目标职位：{{ milestone.metrics.target_role }}</div>
                          <div v-if="milestone.metrics?.target_salary" class="text-xs text-white/60">目标薪资：{{ milestone.metrics.target_salary }}</div>
                        </div>
                        <div class="text-right">
                          <span class="text-xs px-2 py-1 rounded bg-white/5">{{ milestone.category }}</span>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              
              <div v-if="selectedPlan.alternative_paths?.length" class="p-4 bg-white/5 rounded-lg">
                <h4 class="font-medium mb-3">路径对比</h4>
                <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div>
                    <p class="text-xs text-white/60 mb-2">推荐路径</p>
                    <div class="flex flex-wrap gap-1">
                      <span 
                        v-for="id in selectedPlan.recommended_path?.milestone_ids || []" 
                        :key="id"
                        class="text-xs px-2 py-1 bg-star-primary/20 rounded"
                      >
                        {{ getMilestoneTitle(id) }}
                      </span>
                    </div>
                  </div>
                  <div v-for="(path, index) in selectedPlan.alternative_paths" :key="index">
                    <p class="text-xs text-white/60 mb-2">备选{{ index + 1 }}</p>
                    <div class="flex flex-wrap gap-1">
                      <span 
                        v-for="id in path.milestone_ids || []" 
                        :key="id"
                        class="text-xs px-2 py-1 bg-white/10 rounded"
                      >
                        {{ getMilestoneTitle(id) }}
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            <div v-else-if="plans.length" class="text-center text-white/40 py-12">
              <p class="text-4xl mb-4">📋</p>
              <p>请选择一个规划查看详情</p>
            </div>
            
            <div v-else class="text-center text-white/40 py-12">
              <p class="text-4xl mb-4">📋</p>
              <p>暂无规划记录</p>
              <p class="text-sm mt-2">点击左侧按钮生成职业规划</p>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import Sidebar from '../components/Sidebar.vue'
import { diagnosisApi, planApi } from '../api'
import { ElMessage } from 'element-plus'

const formRef = ref(null)
const loading = ref(false)
const diagnosis = ref(null)
const plans = ref([])
const selectedPlan = ref(null)
const activePath = ref('recommended')

const form = ref({
  plan_type: 'short_term',
})

const planTypeNameMap = {
  short_term: '短期规划（1年）',
  mid_term: '中期规划（3年）',
  long_term: '长期规划（5-10年）',
}

const planTypeName = computed(() => {
  return planTypeNameMap[form.value.plan_type]
})

const filteredMilestones = computed(() => {
  if (!selectedPlan.value) return []
  
  const allMilestones = selectedPlan.value.milestones || []
  
  if (activePath.value === 'recommended') {
    const ids = selectedPlan.value.recommended_path?.milestone_ids || []
    return ids.map(id => allMilestones.find(m => m.id === id)).filter(Boolean)
  }
  
  const index = parseInt(activePath.value.split('_')[1])
  if (selectedPlan.value.alternative_paths?.[index]) {
    const ids = selectedPlan.value.alternative_paths[index].milestone_ids || []
    return ids.map(id => allMilestones.find(m => m.id === id)).filter(Boolean)
  }
  
  return allMilestones
})

const getProbabilityClass = (prob) => {
  if (prob >= 0.8) return 'bg-green-500/20 text-green-400'
  if (prob >= 0.6) return 'bg-yellow-500/20 text-yellow-400'
  return 'bg-red-500/20 text-red-400'
}

const getMilestoneClass = (milestone) => {
  const prob = milestone.probability || 0
  if (prob >= 0.8) return 'bg-green-500/20 border-green-400'
  if (prob >= 0.6) return 'bg-yellow-500/20 border-yellow-400'
  return 'bg-red-500/20 border-red-400'
}

const getMilestoneTitle = (id) => {
  if (!selectedPlan.value) return id
  const milestone = selectedPlan.value.milestones?.find(m => m.id === id)
  return milestone?.title || id
}

const selectPlan = (plan) => {
  selectedPlan.value = plan
  activePath.value = 'recommended'
}

const handleGenerate = async () => {
  loading.value = true
  try {
    const response = await planApi.generate({ plan_type: form.value.plan_type })
    plans.value.unshift(response.data)
    selectedPlan.value = response.data
    ElMessage.success('规划生成成功')
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || '生成失败')
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  try {
    const diagRes = await diagnosisApi.latest()
    diagnosis.value = diagRes.data
  } catch {}
  
  try {
    const planRes = await planApi.list()
    plans.value = planRes.data
    if (plans.value.length) {
      selectedPlan.value = plans.value[0]
    }
  } catch {}
})
</script>
