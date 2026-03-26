<template>
    <div class="auth-page">
      <div class="auth-card">
        <h2>Create Account</h2>
        <p v-if="error" class="error">{{ error }}</p>
        <input v-model="username" type="text"     placeholder="Username" />
        <input v-model="email"    type="email"    placeholder="Email" />
        <input v-model="password" type="password" placeholder="Password" />
        <button @click="submit" :disabled="loading">
          {{ loading ? 'Registering...' : 'Register' }}
        </button>
        <p>Already have an account? <router-link to="/login">Login</router-link></p>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  import { useRouter } from 'vue-router'
  import { useAuthStore } from '../stores/auth'
  
  const auth     = useAuthStore()
  const router   = useRouter()
  const username = ref('')
  const email    = ref('')
  const password = ref('')
  const error    = ref('')
  const loading  = ref(false)
  
  async function submit() {
    error.value   = ''
    loading.value = true
    try {
      await auth.register(username.value, email.value, password.value)
      router.push('/login')
    } catch (e) {
      error.value = e.response?.data?.detail || 'Registration failed'
    } finally {
      loading.value = false
    }
  }
  </script>