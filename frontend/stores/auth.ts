import { defineStore } from 'pinia'

interface AdminUser {
  id: number
  username: string
  display_name: string
  is_active: boolean
}

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: '' as string,
    user: null as AdminUser | null,
    _initialized: false,
  }),

  getters: {
    isAuthenticated: (state) => !!state.token,
  },

  actions: {
    async login(username: string, password: string) {
      const api = useApi()
      const res = await api.post<{ access_token: string }>('/auth/login', {
        username,
        password,
      })
      this.token = res.access_token
      this._saveToken()
      await this._fetchUser()
    },

    logout() {
      this.token = ''
      this.user = null
      this._saveToken()
      navigateTo('/admin/login')
    },

    async init() {
      if (this._initialized) return
      this._initialized = true
      if (import.meta.client) {
        const saved = localStorage.getItem('admin_token')
        if (saved) {
          this.token = saved
          await this._fetchUser()
        }
      }
    },

    async _fetchUser() {
      if (!this.token) return
      try {
        const config = useRuntimeConfig()
        const user = await $fetch<AdminUser>(`${config.public.apiBase}/auth/me`, {
          headers: { Authorization: `Bearer ${this.token}` },
        })
        this.user = user
      } catch {
        // token过期或无效，清除
        this.token = ''
        this.user = null
        this._saveToken()
      }
    },

    _saveToken() {
      if (import.meta.client) {
        if (this.token) localStorage.setItem('admin_token', this.token)
        else localStorage.removeItem('admin_token')
      }
    },
  },
})
