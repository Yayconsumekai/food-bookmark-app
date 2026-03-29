<template>
    <div class="auth-page">
      <div class="auth-card">
        <h2>Login</h2>
        <p v-if="error" class="error">{{ error }}</p>
        <input v-model="email"    type="email"    placeholder="Email" />
        <input v-model="password" type="password" placeholder="Password" />
        <button @click="submit" :disabled="loading">
          {{ loading ? 'Logging in...' : 'Login' }}
        </button>
        <p>Don't have an account? <router-link to="/register">Register</router-link></p>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  import { useRouter } from 'vue-router'
  import { useAuthStore } from '../stores/auth'
  
  const auth     = useAuthStore()
  const router   = useRouter()
  const email    = ref('')
  const password = ref('')
  const error    = ref('')
  const loading  = ref(false)
  
  async function submit() {
    error.value   = ''
    loading.value = true
    try {
      await auth.login(email.value, password.value)
      router.push('/')
    } catch (e) {
      error.value = e.response?.data?.detail || 'Login failed'
    } finally {
      loading.value = false
    }
  }
  </script>