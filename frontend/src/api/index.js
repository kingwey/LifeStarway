import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 60000,
})

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export const authApi = {
  register: (data) => api.post('/auth/register', data),
  login: (data) => api.post('/auth/login', data),
  me: () => api.get('/auth/me'),
}

export const profileApi = {
  get: () => api.get('/profiles'),
  update: (data) => api.post('/profiles', data),
  importResume: (data) => api.post('/profiles/import-resume', data),
  uploadResume: (file) => {
    const formData = new FormData()
    formData.append('file', file)
    return api.post('/profiles/upload-resume', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
      timeout: 120000,
    })
  },
  importLinks: (data) => api.post('/profiles/import-links', data),
  versions: () => api.get('/profiles/versions'),
}

export const diagnosisApi = {
  create: (data) => api.post('/diagnoses', data),
  latest: () => api.get('/diagnoses/latest'),
  list: () => api.get('/diagnoses'),
}

export const planApi = {
  generate: (data) => api.post('/plans/generate', data),
  list: () => api.get('/plans'),
  get: (id) => api.get(`/plans/${id}`),
}

export const starmapApi = {
  get: () => api.get('/starmap'),
}

export const simulationApi = {
  create: (data) => api.post('/simulations', data),
  list: () => api.get('/simulations'),
  get: (id) => api.get(`/simulations/${id}`),
}

export default api
