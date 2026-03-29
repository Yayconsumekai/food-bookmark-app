<template>
  <div class="search-page">
    <div class="search-header">
      <SearchBar />
      <ExpansionBanner :expansion="search.expansion" />
      <p v-if="search.total > 0" class="result-count">
        Showing
        {{ (search.currentPage - 1) * search.pageSize + 1 }}–{{ Math.min(search.currentPage * search.pageSize,
          search.total) }}
        of {{ search.total }} results for <strong>"{{ search.query }}"</strong>
        <span v-if="hasActiveFilters" class="filter-indicator">— filtered</span>
      </p>
    </div>

    <!-- Layout: sidebar + results -->
    <div class="search-layout">

      <!-- Facet sidebar — only show when there are results -->
      <FacetSidebar v-if="search.results.length || hasActiveFilters" :facets="search.facets" v-model:filters="filters"
        @apply="applyFilters" />

      <!-- Results area -->
      <div class="results-area">
        <div v-if="search.loading" class="card-grid">
          <div v-for="n in 8" :key="n" class="skeleton-card" />
        </div>

        <div v-else-if="search.results.length" class="card-grid">
          <RecipeCard v-for="r in search.results.filter(r => r.image_url)" :key="r.id" :recipe="r"
            @select="openRecipe(r.id)" />
        </div>

        <div v-else-if="search.query && !search.loading" class="empty-state">
          <p>No results found for <strong>"{{ search.query }}"</strong>.</p>
          <button v-if="hasActiveFilters" @click="clearFilters">
            Clear filters and try again
          </button>
        </div>
        <PaginationBar :current-page="search.currentPage" :total-pages="search.totalPages" @go="search.goToPage" />
      </div>
    </div>
  </div>
</template>

<script setup>
import PaginationBar from '../components/PaginationBar.vue'
import { ref, computed } from 'vue'
import SearchBar from '../components/SearchBar.vue'
import RecipeCard from '../components/RecipeCard.vue'
import ExpansionBanner from '../components/ExpansionBanner.vue'
import FacetSidebar from '../components/FacetSidebar.vue'
import { useSearchStore } from '../stores/search'
import { useRecipeStore } from '../stores/recipe'

const search = useSearchStore()
const recipe = useRecipeStore()

const filters = ref({
  category: null,
  minRating: null,
  maxMinutes: null,
})

const hasActiveFilters = computed(() =>
  Object.values(filters.value).some(v => v !== null)
)

function applyFilters() {
  if (!search.query) return
  search.searchWithFilters(search.query, filters.value)
}

function clearFilters() {
  filters.value = { category: null, minRating: null, maxMinutes: null }
  search.search(search.query)
}

function openRecipe(id) {
  recipe.fetchRecipe(id)
}
</script>

<style scoped>
.search-page {
  max-width: 1300px;
  margin: 0 auto;
  padding: 2rem 1rem;
}

.search-header {
  margin-bottom: 1.5rem;
}

.result-count {
  font-size: 0.9rem;
  color: #666;
  margin-top: 0.5rem;
}

.filter-indicator {
  color: #d97706;
}

.search-layout {
  display: flex;
  gap: 1.5rem;
  align-items: flex-start;
}

.results-area {
  flex: 1;
  min-width: 0;
}

.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1.25rem;
}

.skeleton-card {
  height: 280px;
  border-radius: 12px;
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: shimmer 1.4s infinite;
}

@keyframes shimmer {
  0% {
    background-position: 200% 0;
  }

  100% {
    background-position: -200% 0;
  }
}

.empty-state {
  text-align: center;
  color: #888;
  padding: 4rem 0;
}

.empty-state button {
  margin-top: 1rem;
  background: #f6c90e;
  border: none;
  border-radius: 8px;
  padding: 0.5rem 1rem;
  cursor: pointer;
}

@media (max-width: 700px) {
  .search-layout {
    flex-direction: column;
  }
}
</style>