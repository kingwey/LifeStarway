<template>
  <aside class="w-64 bg-star-deep/50 backdrop-blur-xl border-r border-white/10 h-screen fixed left-0 top-0 z-50">
    <div class="p-6">
      <div class="flex items-center gap-3 mb-8">
        <div class="w-10 h-10 bg-gradient-to-br from-star-primary to-star-secondary rounded-xl flex items-center justify-center">
          <span class="text-xl">🌟</span>
        </div>
        <div>
          <h1 class="text-xl font-bold bg-gradient-to-r from-star-cyan to-star-pink bg-clip-text text-transparent">人生星途</h1>
          <p class="text-xs text-white/50">LifeStarway</p>
        </div>
      </div>
      
      <nav class="space-y-2">
        <router-link
          v-for="item in menuItems"
          :key="item.path"
          :to="item.path"
          class="flex items-center gap-3 px-4 py-3 rounded-xl text-sm transition-all duration-300"
          :class="isActive(item.path) ? 'bg-star-primary/20 text-star-cyan' : 'text-white/60 hover:bg-white/5 hover:text-white'"
        >
          <span class="text-lg">{{ item.icon }}</span>
          <span>{{ item.label }}</span>
        </router-link>
      </nav>
    </div>
    
    <div class="absolute bottom-6 left-6 right-6">
      <div class="flex items-center gap-3 p-3 bg-white/5 rounded-xl">
        <div class="w-10 h-10 bg-gradient-to-br from-star-primary to-star-secondary rounded-full flex items-center justify-center">
          <span class="text-sm">{{ userStore.user?.nickname?.charAt(0) || '?' }}</span>
        </div>
        <div class="flex-1">
          <p class="text-sm font-medium">{{ userStore.user?.nickname }}</p>
          <p class="text-xs text-white/50">{{ userStore.user?.email }}</p>
        </div>
        <button @click="handleLogout" class="text-white/40 hover:text-red-400 transition-colors">
          <span class="text-lg">🚪</span>
        </button>
      </div>
    </div>
  </aside>
</template>

<script setup>
import { useRouter, useRoute } from 'vue-router'
import { useUserStore } from '../stores/user'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

const menuItems = [
  { path: '/', label: '仪表盘', icon: '📊' },
  { path: '/profile', label: '人生档案', icon: '📁' },
  { path: '/diagnosis', label: '职业诊断', icon: '🤖' },
  { path: '/plan', label: '规划方案', icon: '📋' },
  { path: '/starmap', label: '人生星图', icon: '🌌' },
  { path: '/whatif', label: 'What-If', icon: '🔮' },
]

const isActive = (path) => {
  if (path === '/') return route.path === '/'
  return route.path.startsWith(path)
}

const handleLogout = () => {
  userStore.logout()
  router.push('/login')
}
</script>
