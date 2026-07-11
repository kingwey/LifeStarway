import { defineStore } from 'pinia'
import { ref } from 'vue'
import { authApi, profileApi } from '../api'

export const useUserStore = defineStore('user', () => {
  const token = ref(localStorage.getItem('token') || '')
  const user = ref(JSON.parse(localStorage.getItem('user') || 'null'))
  const profile = ref(null)

  const isLoggedIn = () => !!token.value && !!user.value

  const login = async (data) => {
    const response = await authApi.login(data)
    token.value = response.data.access_token
    localStorage.setItem('token', token.value)
    await fetchUser()
    return response.data
  }

  const register = async (data) => {
    const response = await authApi.register(data)
    return response.data
  }

  const fetchUser = async () => {
    try {
      const response = await authApi.me()
      user.value = response.data
      localStorage.setItem('user', JSON.stringify(user.value))
    } catch {
      logout()
    }
  }

  const fetchProfile = async () => {
    try {
      const response = await profileApi.get()
      profile.value = response.data
    } catch {
      profile.value = null
    }
  }

  const logout = () => {
    token.value = ''
    user.value = null
    profile.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  }

  return {
    token,
    user,
    profile,
    isLoggedIn,
    login,
    register,
    fetchUser,
    fetchProfile,
    logout,
  }
})
