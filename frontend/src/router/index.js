import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '../stores/user'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue'),
    meta: { requiresAuth: false },
  },
  {
    path: '/',
    name: 'Dashboard',
    component: () => import('../views/Dashboard.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('../views/Profile.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/diagnosis',
    name: 'Diagnosis',
    component: () => import('../views/Diagnosis.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/plan',
    name: 'Plan',
    component: () => import('../views/Plan.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/starmap',
    name: 'StarMap',
    component: () => import('../views/StarMap.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/whatif',
    name: 'WhatIf',
    component: () => import('../views/WhatIf.vue'),
    meta: { requiresAuth: true },
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  const userStore = useUserStore()
  if (to.meta.requiresAuth && !userStore.isLoggedIn()) {
    next('/login')
  } else if (!to.meta.requiresAuth && userStore.isLoggedIn()) {
    next('/')
  } else {
    next()
  }
})

export default router
