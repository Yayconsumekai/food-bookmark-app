<template>
    <div class="search-wrapper">
      <div class="search-bar">
        <input
          v-model="inputQuery"
          type="text"
          placeholder="Search by dish name, ingredient, or cooking method..."
          @keyup.enter="handleSearch"
        />
        <button @click="handleSearch" :disabled="search.loading">
          {{ search.loading ? '...' : '🔍' }}
        </button>
      </div>
  
      <!-- Spell correction banner sits right under the bar -->
      <SpellBanner />
  
      <p v-if="search.error" class="search-error">{{ search.error }}</p>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  import { useSearchStore } from '../stores/search'
  import SpellBanner from './SpellBanner.vue'
  
  const search     = useSearchStore()
  const inputQuery = ref('')
  
  async function handleSearch() {
    const q = inputQuery.value.trim()
    if (!q) return
  
    // Always clear previous spell state first
    search.clearSpell()
  
    // Check spelling before searching
    const spell = await search.checkSpelling(q)
  
    if (spell?.has_corrections) {
      // SpellBanner will appear — wait for user to confirm
      // (acceptCorrection or rejectCorrection will trigger actual search)
      return
    }
  
    // No typos — search directly
    await search.search(q)
  }
  </script>
  
  <style scoped>
  .search-wrapper { width: 100%; max-width: 700px; margin: 0 auto; }
  .search-bar {
    display:       flex;
    gap:           0.5rem;
  }
  .search-bar input {
    flex:          1;
    padding:       0.75rem 1rem;
    border:        1px solid #ddd;
    border-radius: 8px;
    font-size:     1rem;
    outline:       none;
  }
  .search-bar input:focus { border-color: #f6c90e; }
  .search-bar button {
    padding:       0.75rem 1.25rem;
    background:    #f6c90e;
    border:        none;
    border-radius: 8px;
    font-size:     1.1rem;
    cursor:        pointer;
  }
  .search-error { color: red; font-size: 0.85rem; margin-top: 0.3rem; }
  </style>