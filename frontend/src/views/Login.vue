<template>
  <div class="min-h-screen flex items-center justify-center p-4">
    <div class="absolute inset-0 overflow-hidden">
      <div v-for="i in 100" :key="i" class="star" :style="getStarStyle(i)"></div>
    </div>
    
    <div class="relative z-10 w-full max-w-md">
      <div class="text-center mb-8">
        <div class="w-20 h-20 bg-gradient-to-br from-star-primary to-star-secondary rounded-2xl flex items-center justify-center mx-auto mb-4 shadow-lg shadow-star-primary/25">
          <span class="text-4xl">🌟</span>
        </div>
        <h1 class="text-3xl font-bold bg-gradient-to-r from-star-cyan to-star-pink bg-clip-text text-transparent">人生星途</h1>
        <p class="text-white/60 mt-2">数据沉淀迭代式AI全生命周期职业生涯规划系统</p>
      </div>
      
      <div class="bg-white/5 backdrop-blur-xl rounded-2xl p-8 border border-white/10">
        <el-tabs v-model="activeTab" class="mb-6">
          <el-tab-pane label="登录" name="login"></el-tab-pane>
          <el-tab-pane label="注册" name="register"></el-tab-pane>
        </el-tabs>
        
        <el-form :model="form" :rules="rules" ref="formRef" class="space-y-4">
          <el-form-item prop="email">
            <el-input v-model="form.email" placeholder="邮箱" prefix-icon="📧"></el-input>
          </el-form-item>
          
          <el-form-item prop="password">
            <el-input v-model="form.password" type="password" placeholder="密码" prefix-icon="🔒"></el-input>
          </el-form-item>
          
          <el-form-item v-if="activeTab === 'register'" prop="nickname">
            <el-input v-model="form.nickname" placeholder="昵称" prefix-icon="👤"></el-input>
          </el-form-item>
          
          <el-form-item>
            <el-button 
              type="primary" 
              :loading="loading"
              class="w-full" 
              @click="handleSubmit"
            >
              {{ activeTab === 'login' ? '登录' : '注册' }}
            </el-button>
          </el-form-item>
        </el-form>
        
        <p class="text-center text-white/40 text-sm mt-6">
          Made with ❤️ using TRAE
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../stores/user'
import { ElMessage } from 'element-plus'

const router = useRouter()
const userStore = useUserStore()

const activeTab = ref('login')
const loading = ref(false)
const formRef = ref(null)

const form = reactive({
  email: '',
  password: '',
  nickname: '',
})

const rules = {
  email: [{ required: true, message: '请输入邮箱', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
  nickname: [{ required: true, message: '请输入昵称', trigger: 'blur' }],
}

const handleSubmit = async () => {
  if (!await formRef.value.validate()) return
  
  loading.value = true
  try {
    if (activeTab.value === 'login') {
      await userStore.login({ email: form.email, password: form.password })
      ElMessage.success('登录成功')
      router.push('/')
    } else {
      await userStore.register({ email: form.email, password: form.password, nickname: form.nickname })
      ElMessage.success('注册成功，请登录')
      activeTab.value = 'login'
      form.nickname = ''
    }
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || '操作失败')
  } finally {
    loading.value = false
  }
}

const getStarStyle = (index) => ({
  left: `${Math.random() * 100}%`,
  top: `${Math.random() * 100}%`,
  width: `${Math.random() * 3 + 1}px`,
  height: `${Math.random() * 3 + 1}px`,
  animationDelay: `${Math.random() * 3}s`,
  animationDuration: `${Math.random() * 2 + 2}s`,
})
</script>

<style scoped>
.star {
  position: absolute;
  background: #fff;
  border-radius: 50%;
  animation: twinkle 3s infinite ease-in-out;
}

@keyframes twinkle {
  0%, 100% { opacity: 0.3; transform: scale(1); }
  50% { opacity: 1; transform: scale(1.2); }
}
</style>
