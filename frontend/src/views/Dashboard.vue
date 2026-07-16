<template>
  <div class="min-h-screen">
    <Sidebar />
    <main class="ml-64 p-8">
      <div class="mb-8">
        <h2 class="text-2xl font-bold">仪表盘</h2>
        <p class="text-white/60 mt-1">欢迎回来，{{ userStore.user?.nickname }} · 您的职业规划总览</p>
      </div>
      
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div class="bg-white/5 backdrop-blur-xl rounded-xl p-6 border border-white/10">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-white/60 text-sm">职业健康度</p>
              <p class="text-3xl font-bold mt-2" :class="healthColor">{{ diagnosis?.health_score || '--' }}</p>
            </div>
            <div class="w-14 h-14 bg-star-primary/20 rounded-xl flex items-center justify-center">
              <span class="text-2xl">❤️</span>
            </div>
          </div>
        </div>
        
        <div class="bg-white/5 backdrop-blur-xl rounded-xl p-6 border border-white/10">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-white/60 text-sm">规划方案</p>
              <p class="text-3xl font-bold mt-2">{{ plans.length }}</p>
            </div>
            <div class="w-14 h-14 bg-star-cyan/20 rounded-xl flex items-center justify-center">
              <span class="text-2xl">📋</span>
            </div>
          </div>
        </div>
        
        <div class="bg-white/5 backdrop-blur-xl rounded-xl p-6 border border-white/10">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-white/60 text-sm">里程碑</p>
              <p class="text-3xl font-bold mt-2">{{ milestoneCount }}</p>
            </div>
            <div class="w-14 h-14 bg-star-pink/20 rounded-xl flex items-center justify-center">
              <span class="text-2xl">⭐</span>
            </div>
          </div>
        </div>
        
        <div class="bg-white/5 backdrop-blur-xl rounded-xl p-6 border border-white/10">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-white/60 text-sm">档案版本</p>
              <p class="text-3xl font-bold mt-2">{{ userStore.profile?.version || 0 }}</p>
            </div>
            <div class="w-14 h-14 bg-star-secondary/20 rounded-xl flex items-center justify-center">
              <span class="text-2xl">📁</span>
            </div>
          </div>
        </div>
      </div>
      
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div class="bg-white/5 backdrop-blur-xl rounded-xl p-6 border border-white/10">
          <h3 class="text-lg font-semibold mb-4">职业诊断结果</h3>
          <div v-if="diagnosis" class="space-y-4">
            <div class="flex items-center justify-between">
              <span class="text-white/60">成长性</span>
              <el-progress :percentage="diagnosis.dimensions.growth || 0" :color="getDimensionColor(diagnosis.dimensions.growth)" :stroke-width="12" />
            </div>
            <div class="flex items-center justify-between">
              <span class="text-white/60">稳定性</span>
              <el-progress :percentage="diagnosis.dimensions.stability || 0" :color="getDimensionColor(diagnosis.dimensions.stability)" :stroke-width="12" />
            </div>
            <div class="flex items-center justify-between">
              <span class="text-white/60">收入潜力</span>
              <el-progress :percentage="diagnosis.dimensions.income_potential || 0" :color="getDimensionColor(diagnosis.dimensions.income_potential)" :stroke-width="12" />
            </div>
            <div class="flex items-center justify-between">
              <span class="text-white/60">兴趣匹配</span>
              <el-progress :percentage="diagnosis.dimensions.interest_match || 0" :color="getDimensionColor(diagnosis.dimensions.interest_match)" :stroke-width="12" />
            </div>
            <div class="flex items-center justify-between">
              <span class="text-white/60">行业前景</span>
              <el-progress :percentage="diagnosis.dimensions.industry_outlook || 0" :color="getDimensionColor(diagnosis.dimensions.industry_outlook)" :stroke-width="12" />
            </div>
          </div>
          <div v-else class="text-center text-white/40 py-8">
            <p>暂无诊断记录</p>
            <el-button type="primary" size="small" @click="$router.push('/diagnosis')" class="mt-4">去诊断</el-button>
          </div>
        </div>
        
        <div class="bg-white/5 backdrop-blur-xl rounded-xl p-6 border border-white/10">
          <h3 class="text-lg font-semibold mb-4">最近规划</h3>
          <div v-if="plans.length" class="space-y-3">
            <div v-for="plan in plans.slice(0, 3)" :key="plan.id" class="flex items-center justify-between p-3 bg-white/5 rounded-lg hover:bg-white/10 transition-colors">
              <div>
                <p class="font-medium">{{ plan.title }}</p>
                <p class="text-xs text-white/50">{{ plan.plan_type === 'short_term' ? '短期(1年)' : plan.plan_type === 'mid_term' ? '中期(3年)' : '长期(5-10年)' }}</p>
              </div>
              <span class="text-sm bg-star-primary/20 text-star-cyan px-3 py-1 rounded-full">{{ plan.milestones?.length || 0 }} 个里程碑</span>
            </div>
          </div>
          <div v-else class="text-center text-white/40 py-8">
            <p>暂无规划记录</p>
            <el-button type="primary" size="small" @click="$router.push('/plan')" class="mt-4">去生成</el-button>
          </div>
        </div>
      </div>
      
      <div class="mt-6 bg-white/5 backdrop-blur-xl rounded-xl p-6 border border-white/10">
        <h3 class="text-lg font-semibold mb-4">快速操作</h3>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
          <button @click="$router.push('/profile')" class="p-4 bg-white/5 rounded-xl hover:bg-white/10 transition-colors text-center">
            <span class="text-3xl">📝</span>
            <p class="text-sm mt-2">完善档案</p>
          </button>
          <button @click="$router.push('/diagnosis')" class="p-4 bg-white/5 rounded-xl hover:bg-white/10 transition-colors text-center">
            <span class="text-3xl">🤖</span>
            <p class="text-sm mt-2">职业诊断</p>
          </button>
          <button @click="$router.push('/plan')" class="p-4 bg-white/5 rounded-xl hover:bg-white/10 transition-colors text-center">
            <span class="text-3xl">📋</span>
            <p class="text-sm mt-2">生成规划</p>
          </button>
          <button @click="$router.push('/starmap')" class="p-4 bg-white/5 rounded-xl hover:bg-white/10 transition-colors text-center">
            <span class="text-3xl">🌌</span>
            <p class="text-sm mt-2">查看星图</p>
          </button>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import Sidebar from '../components/Sidebar.vue'
import { useUserStore } from '../stores/user'
import { useAppStore } from '../stores/app'

const userStore = useUserStore()
const appStore = useAppStore()

const diagnosis = computed(() => appStore.latestDiagnosis)
const plans = computed(() => appStore.plans)

const healthColor = computed(() => {
  const score = diagnosis.value?.health_score || 0
  if (score >= 80) return 'text-green-400'
  if (score >= 60) return 'text-yellow-400'
  return 'text-red-400'
})

const milestoneCount = computed(() => appStore.milestoneCount)

const getDimensionColor = (value) => {
  if (value >= 80) return '#4ade80'
  if (value >= 60) return '#facc15'
  return '#f87171'
}

onMounted(async () => {
  await userStore.fetchProfile()
  await appStore.loadAll()
})
</script>
