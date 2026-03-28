<template>
  <NavBar v-if="auth.isLoggedIn" />
  <RouterView />
  <RecipeModal />
</template>

<script setup>
import NavBar     from './components/NavBar.vue'
import RecipeModal from './components/RecipeModal.vue'
import { useAuthStore } from './stores/auth'
import { watch } from 'vue'
import { useRoute } from 'vue-router'

const auth = useAuthStore()
const route = useRoute()
watch(route, () => {
  document.body.style.overflow = ''
})
</script>