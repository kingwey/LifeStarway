<template>
  <div class="min-h-screen">
    <Sidebar />
    <main class="ml-64 p-8">
      <div class="mb-8">
        <h2 class="text-2xl font-bold">What-If 沙盒</h2>
        <p class="text-white/60 mt-1">模拟不同选择，探索您的人生轨迹变化</p>
      </div>
      
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
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
                  <el-option label="读MBA" value="读MBA"></el-option>
                  <el-option label="跳槽" value="跳槽"></el-option>
                  <el-option label="创业" value="创业"></el-option>
                  <el-option label="深耕当前领域" value="深耕当前领域"></el-option>
                </el-select>
              </el-form-item>
              
              <el-form-item label="目标行业/方向">
                <el-input v-model="form.hypothesis.target_industry" placeholder="如：AI、金融、教育"></el-input>
              </el-form-item>
              
              <el-form-item label="预期时间">
                <el-input v-model="form.hypothesis.timeframe" placeholder="如：1年内、3年内"></el-input>
              </el-form-item>
              
              <el-form-item label="备注说明">
                <el-textarea v-model="form.hypothesis.note" rows="3" placeholder="其他补充信息"></el-textarea>
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
        
        <div class="bg-white/5 backdrop-blur-xl rounded-xl p-6 border border-white/10">
          <h3 class="text-lg font-semibold mb-4">模拟结果</h3>
          
          <div v-if="simulation" class="space-y-6">
            <div>
              <h4 class="font-medium mb-2">假设条件</h4>
              <div class="p-3 bg-white/5 rounded-lg">
                <p class="text-sm">
                  <span class="text-star-cyan">{{ simulation.hypothesis.action }}</span>
                  → {{ simulation.hypothesis.target_industry || '-' }}
                  <span v-if="simulation.hypothesis.timeframe" class="text-white/50">（{{ simulation.hypothesis.timeframe }}）</span>
                </p>
                <p v-if="simulation.hypothesis.note" class="text-xs text-white/60 mt-1">{{ simulation.hypothesis.note }}</p>
              </div>
            </div>
            
            <div>
              <h4 class="font-medium mb-2">模拟里程碑</h4>
              <div class="space-y-2">
                <div v-for="(milestone, index) in simulation.simulated_milestones" :key="index" class="p-3 bg-white/5 rounded-lg">
                  <div class="flex items-center justify-between">
                    <span class="font-medium text-sm">{{ milestone.title }}</span>
                    <span class="text-xs px-2 py-0.5 rounded-full" :class="getProbabilityClass(milestone.probability)">{{ Math.round(milestone.probability * 100) }}%</span>
                  </div>
                  <p class="text-xs text-white/50 mt-1">{{ milestone.target_date }}</p>
                </div>
              </div>
            </div>
            
            <div>
              <h4 class="font-medium mb-2">风险评估</h4>
              <div class="p-3 bg-white/5 rounded-lg">
                <div class="flex items-center gap-2 mb-2">
                  <span class="text-sm font-medium">风险等级：</span>
                  <span class="px-2 py-0.5 rounded-full text-xs" :class="getRiskClass(simulation.risk_assessment.risk_level)">
                    {{ simulation.risk_assessment.risk_level || '-' }}
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
              <h4 class="font-medium mb-2">路径对比</h4>
              <div class="p-3 bg-white/5 rounded-lg">
                <p class="text-sm mb-2">
                  <span class="text-white/60">原路径：</span>
                  <span>{{ simulation.comparison.original_path || '-' }}</span>
                </p>
                <p class="text-sm mb-2">
                  <span class="text-white/60">模拟路径：</span>
                  <span class="text-star-cyan">{{ simulation.comparison.simulated_path || '-' }}</span>
                </p>
                <div v-if="simulation.comparison.key_differences?.length" class="space-y-1 mt-2">
                  <p v-for="(diff, index) in simulation.comparison.key_differences" :key="index" class="text-xs text-white/60">• {{ diff }}</p>
                </div>
                <p v-if="simulation.comparison.recommendation" class="mt-3 text-xs text-star-cyan">
                  💡 {{ simulation.comparison.recommendation }}
                </p>
              </div>
            </div>
          </div>
          
          <div v-else class="text-center text-white/40 py-12">
            <p class="text-4xl mb-4">🔮</p>
            <p>暂无模拟记录</p>
            <p class="text-sm mt-2">设置假设条件，探索不同选择的可能</p>
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
import { simulationApi } from '../api'
import { ElMessage } from 'element-plus'

const userStore = useUserStore()
const formRef = ref(null)
const loading = ref(false)
const simulation = ref(null)

const form = reactive({
  hypothesis: {
    action: '',
    target_industry: '',
    timeframe: '',
    note: ''
  }
})

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

const handleSimulate = async () => {
  if (!form.hypothesis.action) {
    ElMessage.warning('请选择假设场景')
    return
  }
  
  loading.value = true
  try {
    const response = await simulationApi.create({ hypothesis: form.hypothesis })
    simulation.value = response.data
    ElMessage.success('模拟完成')
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || '模拟失败')
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  await userStore.fetchProfile()
})
</script>
