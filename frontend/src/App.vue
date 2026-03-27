<template>
  <NavBar v-if="auth.isLoggedIn" />
  <RouterView />
  <RecipeModal />
</template>

<script setup>
import NavBar     from './components/NavBar.vue'
import RecipeModal from './components/RecipeModal.vue'
import { useAuthStore } from './stores/auth'

const auth = useAuthStore()
</script>