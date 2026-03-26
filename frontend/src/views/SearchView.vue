<template>
    <div class="search-page">
      <div class="search-header">
        <SearchBar />
        <p v-if="search.total > 0" class="result-count">
          {{ search.total }} results for <strong>"{{ search.query }}"</strong>
        </p>
      </div>
  
      <!-- Loading skeleton -->
      <div v-if="search.loading" class="card-grid">
        <div v-for="n in 8" :key="n" class="skeleton-card" />
      </div>
  
      <!-- Results grid -->
      <div v-else-if="search.results.length" class="card-grid">
        <RecipeCard
          v-for="recipe in search.results"
          :key="recipe.id"
          :recipe="recipe"
          @select="selectedRecipe = recipe"
        />
      </div>
  
      <!-- Empty state -->
      <div v-else-if="search.query && !search.loading" class="empty-state">
        <p>No results found for <strong>"{{ search.query }}"</strong>. Try different keywords.</p>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  import SearchBar  from '../components/SearchBar.vue'
  import RecipeCard from '../components/RecipeCard.vue'
  import { useSearchStore } from '../stores/search'
  
  const search         = useSearchStore()
  const selectedRecipe = ref(null)   // we'll wire this to a modal in Step 5
  </script>
  
  <style scoped>
  .search-page   { max-width: 1200px; margin: 0 auto; padding: 2rem 1rem; }
  .search-header { margin-bottom: 2rem; }
  .result-count  { font-size: 0.9rem; color: #666; margin-top: 0.5rem; }
  
  .card-grid {
    display:                grid;
    grid-template-columns:  repeat(auto-fill, minmax(220px, 1fr));
    gap:                    1.25rem;
  }
  
  /* Skeleton loading animation */
  .skeleton-card {
    height:         280px;
    border-radius:  12px;
    background:     linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
    background-size: 200% 100%;
    animation:      shimmer 1.4s infinite;
  }
  @keyframes shimmer {
    0%   { background-position: 200% 0; }
    100% { background-position: -200% 0; }
  }
  
  .empty-state { text-align: center; color: #888; padding: 4rem 0; }
  </style>