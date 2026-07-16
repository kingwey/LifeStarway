import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { profileApi, diagnosisApi, planApi, simulationApi } from '../api'

export const useAppStore = defineStore('app', () => {
  // 全局状态
  const profile = ref(null)
  const diagnoses = ref([])
  const plans = ref([])
  const simulations = ref([])
  const latestDiagnosis = ref(null)
  const loading = ref({
    profile: false,
    diagnoses: false,
    plans: false,
    simulations: false,
  })
  const error = ref(null)

  const isProfileLoaded = computed(() => !!profile.value)
  const hasDiagnoses = computed(() => diagnoses.value.length > 0)
  const hasPlans = computed(() => plans.value.length > 0)
  const milestoneCount = computed(() => {
    if (!Array.isArray(plans.value)) return 0
    return plans.value.reduce((sum, plan) => sum + (plan.milestones?.length || 0), 0)
  })

  // Profile
  const fetchProfile = async () => {
    loading.value.profile = true
    error.value = null
    try {
      const response = await profileApi.get()
      profile.value = response.data
    } catch (e) {
      error.value = e.response?.data?.detail || '获取档案失败'
      console.warn('获取档案失败:', e.message)
      profile.value = null
    } finally {
      loading.value.profile = false
    }
  }

  const updateProfile = async (data) => {
    error.value = null
    try {
      const response = await profileApi.update(data)
      profile.value = response.data
      return response.data
    } catch (e) {
      error.value = e.response?.data?.detail || '更新档案失败'
      throw e
    }
  }

  // Diagnoses
  const fetchDiagnoses = async () => {
    loading.value.diagnoses = true
    error.value = null
    try {
      const response = await diagnosisApi.list()
      diagnoses.value = response.data || []
      if (diagnoses.value.length) {
        latestDiagnosis.value = diagnoses.value[0]
      }
    } catch (e) {
      error.value = e.response?.data?.detail || '获取诊断失败'
      console.warn('获取诊断失败:', e.message)
    } finally {
      loading.value.diagnoses = false
    }
  }

  const createDiagnosis = async (data = {}) => {
    error.value = null
    try {
      const response = await diagnosisApi.create(data)
      diagnoses.value.unshift(response.data)
      latestDiagnosis.value = response.data
      return response.data
    } catch (e) {
      error.value = e.response?.data?.detail || '创建诊断失败'
      throw e
    }
  }

  // Plans
  const fetchPlans = async () => {
    loading.value.plans = true
    error.value = null
    try {
      const response = await planApi.list()
      plans.value = response.data || []
    } catch (e) {
      error.value = e.response?.data?.detail || '获取规划失败'
      console.warn('获取规划失败:', e.message)
    } finally {
      loading.value.plans = false
    }
  }

  const generatePlan = async (data) => {
    error.value = null
    try {
      const response = await planApi.generate(data)
      plans.value.unshift(response.data)
      return response.data
    } catch (e) {
      error.value = e.response?.data?.detail || '生成规划失败'
      throw e
    }
  }

  // Simulations
  const fetchSimulations = async () => {
    loading.value.simulations = true
    error.value = null
    try {
      const response = await simulationApi.list()
      simulations.value = response.data || []
    } catch (e) {
      error.value = e.response?.data?.detail || '获取模拟失败'
      console.warn('获取模拟失败:', e.message)
    } finally {
      loading.value.simulations = false
    }
  }

  const createSimulation = async (data) => {
    error.value = null
    try {
      const response = await simulationApi.create(data)
      simulations.value.unshift(response.data)
      return response.data
    } catch (e) {
      error.value = e.response?.data?.detail || '创建模拟失败'
      throw e
    }
  }

  // 一键加载所有数据（用于Dashboard等入口页面）
  const loadAll = async () => {
    await fetchProfile()
    await Promise.all([
      fetchDiagnoses().catch(() => {}),
      fetchPlans().catch(() => {}),
      fetchSimulations().catch(() => {}),
    ])
  }

  // 清除所有状态
  const clearAll = () => {
    profile.value = null
    diagnoses.value = []
    plans.value = []
    simulations.value = []
    latestDiagnosis.value = null
    error.value = null
  }

  return {
    profile,
    diagnoses,
    plans,
    simulations,
    latestDiagnosis,
    loading,
    error,
    isProfileLoaded,
    hasDiagnoses,
    hasPlans,
    milestoneCount,
    fetchProfile,
    updateProfile,
    fetchDiagnoses,
    createDiagnosis,
    fetchPlans,
    generatePlan,
    fetchSimulations,
    createSimulation,
    loadAll,
    clearAll,
  }
})
