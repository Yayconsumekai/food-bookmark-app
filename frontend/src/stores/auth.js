import { defineStore } from 'pinia'
import api from '../api/index.js'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user:  JSON.parse(localStorage.getItem('user')) || null,
    token: localStorage.getItem('token') || null,
  }),

  getters: {
    isLoggedIn: (state) => !!state.token,
  },

  actions: {
    async register(username, email, password) {
      const { data } = await api.post('/api/auth/register', {
        username, email, password
      })
      return data
    },

    async login(email, password) {
      const { data } = await api.post('/api/auth/login', { email, password })
      this.token = data.access_token
      this.user  = data.user
      localStorage.setItem('token', this.token)
      localStorage.setItem('user',  JSON.stringify(this.user))
    },

    logout() {
      this.token = null
      this.user  = null
      localStorage.removeItem('token')
      localStorage.removeItem('user')
    },
  },
})