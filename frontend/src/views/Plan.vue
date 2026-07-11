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
        </div>
        
        <div class="lg:col-span-2">
          <div class="bg-white/5 backdrop-blur-xl rounded-xl p-6 border border-white/10">
            <h3 class="text-lg font-semibold mb-4">我的规划</h3>
            
            <div v-if="plans.length" class="space-y-6">
              <div v-for="plan in plans" :key="plan.id" class="border border-white/10 rounded-xl p-4">
                <div class="flex items-center justify-between mb-4">
                  <div>
                    <h4 class="font-bold">{{ plan.title }}</h4>
                    <p class="text-sm text-white/50">{{ planTypeNameMap[plan.plan_type] }}</p>
                  </div>
                  <span class="text-sm bg-star-primary/20 text-star-cyan px-3 py-1 rounded-full">{{ plan.milestones?.length || 0 }} 个里程碑</span>
                </div>
                
                <p class="text-white/80 text-sm mb-4">{{ plan.description }}</p>
                
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3 mb-4">
                  <div v-for="(milestone, index) in plan.milestones" :key="index" class="p-3 bg-white/5 rounded-lg">
                    <div class="flex items-center justify-between">
                      <span class="font-medium text-sm">{{ milestone.title }}</span>
                      <span class="text-xs px-2 py-0.5 rounded-full" :class="getProbabilityClass(milestone.probability)">{{ Math.round(milestone.probability * 100) }}%</span>
                    </div>
                    <p class="text-xs text-white/50 mt-1">{{ milestone.target_date }}</p>
                    <div v-if="milestone.metrics?.target_role" class="text-xs text-white/60 mt-1">{{ milestone.metrics.target_role }}</div>
                  </div>
                </div>
                
                <div v-if="plan.recommended_path" class="mb-3">
                  <p class="text-sm font-medium text-star-cyan">推荐路径：{{ plan.recommended_path.name }}</p>
                  <p class="text-xs text-white/60">{{ plan.recommended_path.description }}</p>
                </div>
                
                <div v-if="plan.alternative_paths?.length" class="flex flex-wrap gap-2">
                  <span v-for="(path, index) in plan.alternative_paths" :key="index" class="text-xs px-3 py-1 bg-white/5 rounded-full text-white/60">备选：{{ path.name }}</span>
                </div>
              </div>
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

const getProbabilityClass = (prob) => {
  if (prob >= 0.8) return 'bg-green-500/20 text-green-400'
  if (prob >= 0.6) return 'bg-yellow-500/20 text-yellow-400'
  return 'bg-red-500/20 text-red-400'
}

const handleGenerate = async () => {
  loading.value = true
  try {
    const response = await planApi.generate({ plan_type: form.value.plan_type })
    plans.value.unshift(response.data)
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
  } catch {}
})
</script>
