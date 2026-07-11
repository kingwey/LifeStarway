<template>
  <div class="min-h-screen">
    <Sidebar />
    <main class="ml-64 p-8">
      <div class="mb-8">
        <h2 class="text-2xl font-bold">职业诊断</h2>
        <p class="text-white/60 mt-1">AI智能评估您的职业健康度，发现优势与风险</p>
      </div>
      
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div class="lg:col-span-1">
          <div class="bg-white/5 backdrop-blur-xl rounded-xl p-6 border border-white/10">
            <h3 class="text-lg font-semibold mb-4">开始诊断</h3>
            <div v-if="!userStore.profile" class="text-center text-white/40 py-8">
              <p>请先完善人生档案</p>
              <el-button type="primary" size="small" @click="$router.push('/profile')" class="mt-4">去完善</el-button>
            </div>
            <div v-else>
              <p class="text-sm text-white/60 mb-4">基于您的档案数据进行AI分析，预计需要 10-30 秒</p>
              <el-button 
                type="primary" 
                :loading="loading"
                class="w-full"
                @click="handleDiagnose"
              >
                🤖 开始AI诊断
              </el-button>
            </div>
          </div>
        </div>
        
        <div class="lg:col-span-2">
          <div class="bg-white/5 backdrop-blur-xl rounded-xl p-6 border border-white/10">
            <h3 class="text-lg font-semibold mb-4">诊断结果</h3>
            
            <div v-if="diagnosis" class="space-y-6">
              <div class="flex items-center justify-between">
                <div>
                  <p class="text-white/60">综合健康度</p>
                  <p class="text-5xl font-bold mt-2" :class="healthColor">{{ diagnosis.health_score }}</p>
                </div>
                <div class="w-24 h-24 rounded-full flex items-center justify-center" :class="healthBg">
                  <span class="text-4xl">{{ healthEmoji }}</span>
                </div>
              </div>
              
              <div class="grid grid-cols-1 md:grid-cols-5 gap-4">
                <div v-for="(value, key) in diagnosis.dimensions" :key="key" class="text-center p-3 bg-white/5 rounded-lg">
                  <p class="text-lg font-bold" :class="getDimensionColor(value)">{{ value }}</p>
                  <p class="text-xs text-white/50 mt-1">{{ dimensionLabels[key] }}</p>
                </div>
              </div>
              
              <div>
                <h4 class="font-medium mb-2">优势分析</h4>
                <div class="flex flex-wrap gap-2">
                  <span v-for="(item, index) in diagnosis.strengths" :key="index" class="px-3 py-1 bg-green-500/20 text-green-400 rounded-full text-sm">{{ item }}</span>
                </div>
              </div>
              
              <div>
                <h4 class="font-medium mb-2">风险提示</h4>
                <div class="flex flex-wrap gap-2">
                  <span v-for="(item, index) in diagnosis.risks" :key="index" class="px-3 py-1 bg-red-500/20 text-red-400 rounded-full text-sm">{{ item }}</span>
                </div>
              </div>
              
              <div>
                <h4 class="font-medium mb-2">诊断总结</h4>
                <p class="text-white/80 leading-relaxed">{{ diagnosis.summary }}</p>
              </div>
              
              <el-button type="primary" @click="$router.push('/plan')">📋 生成职业规划</el-button>
            </div>
            
            <div v-else class="text-center text-white/40 py-12">
              <p class="text-4xl mb-4">🤖</p>
              <p>暂无诊断记录</p>
              <p class="text-sm mt-2">点击左侧按钮开始AI职业诊断</p>
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
import { useUserStore } from '../stores/user'
import { diagnosisApi } from '../api'
import { ElMessage } from 'element-plus'

const userStore = useUserStore()
const diagnosis = ref(null)
const loading = ref(false)

const dimensionLabels = {
  growth: '成长性',
  stability: '稳定性',
  income_potential: '收入潜力',
  interest_match: '兴趣匹配',
  industry_outlook: '行业前景',
}

const healthColor = computed(() => {
  const score = diagnosis.value?.health_score || 0
  if (score >= 80) return 'text-green-400'
  if (score >= 60) return 'text-yellow-400'
  return 'text-red-400'
})

const healthBg = computed(() => {
  const score = diagnosis.value?.health_score || 0
  if (score >= 80) return 'bg-green-500/20'
  if (score >= 60) return 'bg-yellow-500/20'
  return 'bg-red-500/20'
})

const healthEmoji = computed(() => {
  const score = diagnosis.value?.health_score || 0
  if (score >= 80) return '🎉'
  if (score >= 60) return '💪'
  return '⚠️'
})

const getDimensionColor = (value) => {
  if (value >= 80) return 'text-green-400'
  if (value >= 60) return 'text-yellow-400'
  return 'text-red-400'
}

const handleDiagnose = async () => {
  loading.value = true
  try {
    const response = await diagnosisApi.create({})
    diagnosis.value = response.data
    ElMessage.success('诊断完成')
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || '诊断失败')
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  await userStore.fetchProfile()
  try {
    const response = await diagnosisApi.latest()
    diagnosis.value = response.data
  } catch {}
})
</script>
