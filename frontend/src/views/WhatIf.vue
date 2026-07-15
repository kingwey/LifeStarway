<template>
  <div class="min-h-screen">
    <Sidebar />
    <main class="ml-64 p-8">
      <div class="mb-8">
        <h2 class="text-2xl font-bold">What-If 沙盒</h2>
        <p class="text-white/60 mt-1">模拟不同选择，探索您的人生轨迹变化</p>
      </div>
      
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div class="lg:col-span-1">
          <div class="bg-white/5 backdrop-blur-xl rounded-xl p-6 border border-white/10">
            <h3 class="text-lg font-semibold mb-4">创建模拟</h3>
            
            <div v-if="!userStore.profile" class="text-center text-white/40 py-8">
              <p>请先完善人生档案</p>
              <el-button type="primary" size="small" @click="$router.push('/profile')" class="mt-4">去完善</el-button>
            </div>
            
            <div v-else>
              <el-form :model="form" ref="formRef" class="space-y-4">
                <el-form-item label="假设场景">
                  <el-select v-model="form.hypothesis.action" placeholder="选择假设场景">
                    <el-option label="转行" value="转行"></el-option>
                    <el-option label="读MBA/深造" value="读MBA"></el-option>
                    <el-option label="跳槽到大厂" value="跳槽"></el-option>
                    <el-option label="创业" value="创业"></el-option>
                    <el-option label="深耕当前领域" value="深耕当前领域"></el-option>
                    <el-option label="自由职业" value="自由职业"></el-option>
                    <el-option label="出国留学" value="出国留学"></el-option>
                  </el-select>
                </el-form-item>
                
                <el-form-item label="目标行业/方向">
                  <el-input v-model="form.hypothesis.target_industry" placeholder="如：AI、金融、教育、新能源"></el-input>
                </el-form-item>
                
                <el-form-item label="预期时间">
                  <el-select v-model="form.hypothesis.timeframe" placeholder="请选择">
                    <el-option label="6个月内" value="6个月内"></el-option>
                    <el-option label="1年内" value="1年内"></el-option>
                    <el-option label="2年内" value="2年内"></el-option>
                    <el-option label="3年内" value="3年内"></el-option>
                    <el-option label="5年内" value="5年内"></el-option>
                  </el-select>
                </el-form-item>
                
                <el-form-item label="投入资源">
                  <el-select v-model="form.hypothesis.resource_level" placeholder="请选择">
                    <el-option label="低投入（兼职/业余）" value="low"></el-option>
                    <el-option label="中投入（平衡工作学习）" value="medium"></el-option>
                    <el-option label="高投入（全职/全力）" value="high"></el-option>
                  </el-select>
                </el-form-item>
                
                <el-form-item label="备注说明">
                  <el-textarea v-model="form.hypothesis.note" rows="3" placeholder="其他补充信息，如：已有相关经验、家庭支持情况等"></el-textarea>
                </el-form-item>
                
                <el-button 
                  type="primary" 
                  :loading="loading"
                  class="w-full"
                  @click="handleSimulate"
                >
                  🔮 开始模拟
                </el-button>
              </el-form>
              
              <div class="mt-6 p-4 bg-white/5 rounded-lg">
                <p class="text-sm text-white/60">
                  💡 提示：What-If 模拟基于您的当前档案和AI分析，展示假设选择后的职业轨迹变化，供决策参考。
                </p>
              </div>
            </div>
          </div>
          
          <div v-if="simulations.length" class="mt-6 bg-white/5 backdrop-blur-xl rounded-xl p-6 border border-white/10">
            <h3 class="text-lg font-semibold mb-4">历史模拟</h3>
            <div class="space-y-2">
              <div 
                v-for="sim in simulations" 
                :key="sim.id"
                class="p-3 bg-white/5 rounded-lg cursor-pointer hover:bg-white/10 transition-colors"
                :class="{ 'bg-star-primary/20': simulation?.id === sim.id }"
                @click="selectSimulation(sim)"
              >
                <p class="text-sm">{{ sim.hypothesis.action }} → {{ sim.hypothesis.target_industry || '-' }}</p>
                <p class="text-xs text-white/50">{{ formatDate(sim.created_at) }}</p>
              </div>
            </div>
          </div>
        </div>
        
        <div class="lg:col-span-2">
          <div class="bg-white/5 backdrop-blur-xl rounded-xl p-6 border border-white/10">
            <div v-if="simulation" class="space-y-6">
              <div class="flex items-center justify-between">
                <h3 class="text-lg font-semibold">模拟结果</h3>
                <span class="text-xs px-2 py-1 rounded-full" :class="getRiskClass(simulation.risk_assessment.risk_level)">
                  风险：{{ simulation.risk_assessment.risk_level || '-' }}
                </span>
              </div>
              
              <div>
                <h4 class="font-medium mb-2">假设条件</h4>
                <div class="p-3 bg-white/5 rounded-lg">
                  <p class="text-sm">
                    <span class="text-star-cyan">{{ simulation.hypothesis.action }}</span>
                    → {{ simulation.hypothesis.target_industry || '-' }}
                    <span v-if="simulation.hypothesis.timeframe" class="text-white/50">（{{ simulation.hypothesis.timeframe }}）</span>
                  </p>
                  <p v-if="simulation.hypothesis.resource_level" class="text-xs text-white/60 mt-1">
                    投入资源：{{ resourceLevelMap[simulation.hypothesis.resource_level] }}
                  </p>
                  <p v-if="simulation.hypothesis.note" class="text-xs text-white/60">{{ simulation.hypothesis.note }}</p>
                </div>
              </div>
              
              <div>
                <h4 class="font-medium mb-4">路径对比</h4>
                <div class="grid grid-cols-2 gap-4">
                  <div class="bg-white/5 rounded-lg p-4">
                    <div class="flex items-center gap-2 mb-3">
                      <span class="w-3 h-3 rounded-full bg-white/60"></span>
                      <span class="text-sm font-medium">原路径</span>
                    </div>
                    <div class="relative">
                      <div class="absolute left-2 top-0 bottom-0 w-0.5 bg-white/20"></div>
                      <div class="space-y-3">
                        <div 
                          v-for="(milestone, index) in originalMilestones" 
                          :key="index"
                          class="relative pl-6"
                        >
                          <div class="absolute left-0 w-4 h-4 rounded-full bg-white/40 flex items-center justify-center">
                            <div class="w-2 h-2 rounded-full bg-white"></div>
                          </div>
                          <div class="text-xs">
                            <p>{{ milestone.title }}</p>
                            <p class="text-white/50">{{ milestone.target_date }}</p>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  <div class="bg-white/5 rounded-lg p-4">
                    <div class="flex items-center gap-2 mb-3">
                      <span class="w-3 h-3 rounded-full bg-star-cyan"></span>
                      <span class="text-sm font-medium">模拟路径</span>
                    </div>
                    <div class="relative">
                      <div class="absolute left-2 top-0 bottom-0 w-0.5 bg-star-cyan/40"></div>
                      <div class="space-y-3">
                        <div 
                          v-for="(milestone, index) in simulation.simulated_milestones" 
                          :key="index"
                          class="relative pl-6"
                        >
                          <div class="absolute left-0 w-4 h-4 rounded-full bg-star-cyan/40 flex items-center justify-center">
                            <div class="w-2 h-2 rounded-full bg-star-cyan"></div>
                          </div>
                          <div class="text-xs">
                            <p>{{ milestone.title }}</p>
                            <p class="text-white/50">{{ milestone.target_date }}</p>
                            <span class="text-xs px-2 py-0.5 rounded-full" :class="getProbabilityClass(milestone.probability)">{{ Math.round(milestone.probability * 100) }}%</span>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              
              <div>
                <h4 class="font-medium mb-2">风险评估</h4>
                <div class="p-3 bg-white/5 rounded-lg">
                  <div class="flex items-center gap-2 mb-2">
                    <span class="text-sm font-medium">风险等级：</span>
                    <span class="px-2 py-0.5 rounded-full text-xs" :class="getRiskClass(simulation.risk_assessment.risk_level)">
                      {{ riskLevelMap[simulation.risk_assessment.risk_level] || '-' }}
                    </span>
                  </div>
                  <div v-if="simulation.risk_assessment.risks?.length" class="space-y-1">
                    <p v-for="(risk, index) in simulation.risk_assessment.risks" :key="index" class="text-xs text-red-400">• {{ risk }}</p>
                  </div>
                  <div v-if="simulation.risk_assessment.mitigation?.length" class="mt-2">
                    <p class="text-xs text-green-400 font-medium mb-1">应对策略：</p>
                    <p v-for="(item, index) in simulation.risk_assessment.mitigation" :key="index" class="text-xs text-white/60">• {{ item }}</p>
                  </div>
                </div>
              </div>
              
              <div>
                <h4 class="font-medium mb-2">关键差异</h4>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-2">
                  <div v-for="(diff, index) in simulation.comparison.key_differences" :key="index" class="p-2 bg-white/5 rounded text-xs text-white/60">
                    • {{ diff }}
                  </div>
                </div>
              </div>
              
              <div class="p-4 bg-star-primary/10 rounded-lg border border-star-primary/30">
                <p class="text-sm text-star-cyan font-medium mb-1">💡 AI 建议</p>
                <p class="text-xs text-white/80">{{ simulation.comparison.recommendation }}</p>
              </div>
            </div>
            
            <div v-else class="text-center text-white/40 py-12">
              <p class="text-4xl mb-4">🔮</p>
              <p>暂无模拟记录</p>
              <p class="text-sm mt-2">设置假设条件，探索不同选择的可能</p>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import Sidebar from '../components/Sidebar.vue'
import { useUserStore } from '../stores/user'
import { simulationApi, planApi } from '../api'
import { ElMessage } from 'element-plus'

const userStore = useUserStore()
const formRef = ref(null)
const loading = ref(false)
const simulation = ref(null)
const simulations = ref([])
const originalMilestones = ref([])

const resourceLevelMap = {
  low: '低投入（兼职/业余）',
  medium: '中投入（平衡工作学习）',
  high: '高投入（全职/全力）',
}

const riskLevelMap = {
  low: '低风险',
  medium: '中风险',
  high: '高风险',
}

const form = reactive({
  hypothesis: {
    action: '',
    target_industry: '',
    timeframe: '',
    resource_level: 'medium',
    note: ''
  }
})

const formatDate = (dateStr) => {
  if (!dateStr) return '-'
  const date = new Date(dateStr)
  return `${date.getMonth() + 1}/${date.getDate()} ${date.getHours()}:${String(date.getMinutes()).padStart(2, '0')}`
}

const getProbabilityClass = (prob) => {
  if (prob >= 0.8) return 'bg-green-500/20 text-green-400'
  if (prob >= 0.6) return 'bg-yellow-500/20 text-yellow-400'
  return 'bg-red-500/20 text-red-400'
}

const getRiskClass = (level) => {
  if (!level) return 'bg-white/10 text-white/60'
  if (level === 'low') return 'bg-green-500/20 text-green-400'
  if (level === 'medium') return 'bg-yellow-500/20 text-yellow-400'
  return 'bg-red-500/20 text-red-400'
}

const selectSimulation = (sim) => {
  simulation.value = sim
}

const handleSimulate = async () => {
  if (!form.hypothesis.action) {
    ElMessage.warning('请选择假设场景')
    return
  }
  
  loading.value = true
  try {
    const response = await simulationApi.create({ hypothesis: form.hypothesis })
    simulation.value = response.data
    await fetchSimulations()
    ElMessage.success('模拟完成')
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || '模拟失败')
  } finally {
    loading.value = false
  }
}

const fetchSimulations = async () => {
  try {
    const response = await simulationApi.list()
    simulations.value = response.data
  } catch {}
}

const fetchOriginalPlan = async () => {
  try {
    const response = await planApi.list()
    const plans = response.data
    if (plans.length) {
      originalMilestones.value = plans[0].milestones || []
    }
  } catch {}
}

onMounted(async () => {
  await userStore.fetchProfile()
  await fetchSimulations()
  await fetchOriginalPlan()
})
</script>
