<template>
  <RouterView />
  <RecipeModal />   <!-- global modal, rendered once at root -->
</template>

<script setup>
import RecipeModal from './components/RecipeModal.vue'
</script>