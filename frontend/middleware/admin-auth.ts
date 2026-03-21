import { useAuthStore } from '~/stores/auth'

export default defineNuxtRouteMiddleware(async (to) => {
  if (!import.meta.client) return

  const authStore = useAuthStore()
  // 确保从 localStorage 恢复 token 和用户信息
  await authStore.init()

  if (to.path.startsWith('/admin') && to.path !== '/admin/login') {
    if (!authStore.isAuthenticated) {
      return navigateTo('/admin/login')
    }
  }
})
