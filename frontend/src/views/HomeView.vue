<template>
    <div class="home-page">
  
      <!-- Hero banner -->
      <section class="hero">
        <div class="hero-content">
          <h1>
            Hello, <span class="hero-name">{{ auth.user?.username }}</span> 👋
          </h1>
          <p>Discover, save, and organise your favourite recipes.</p>
          <router-link to="/search" class="btn-search-hero">
            🔍 Search Recipes
          </router-link>
        </div>
      </section>
  
      <div class="home-content">
  
        <!-- List 1: For You -->
        <RecipeRow
          title="✨ For You"
          subtitle="Based on your saved recipes"
          :recipes="recs.forYou"
          :loading="recs.loading"
          empty-text="Bookmark some recipes to get personalised suggestions!"
          @select="openRecipe"
        />
  
        <!-- List 2: Browse by Category -->
        <section class="category-section">
          <RecipeRow
            :title="`🍽️ ${recs.byCategory.category}`"
            subtitle="Top recipes in this category"
            :recipes="recs.byCategory.recipes"
            :loading="recs.loading"
            @select="openRecipe"
          >
            <template #header-action>
              <CategoryPicker
                v-model="selectedCategory"
                :categories="recs.categories"
              />
            </template>
          </RecipeRow>
        </section>
  
        <!-- List 3: Discover (random) -->
        <RecipeRow
          title="🎲 Discover Something New"
          subtitle="A random selection just for you"
          :recipes="recs.discover"
          :loading="recs.loading"
          empty-text="Nothing here yet."
          @select="openRecipe"
        >
          <template #header-action>
            <button class="btn-refresh" @click="recs.fetchLanding(selectedCategory)">
              🔄 Shuffle
            </button>
          </template>
        </RecipeRow>
  
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, watch, onMounted } from 'vue'
  import { useAuthStore }            from '../stores/auth'
  import { useRecommendationStore }  from '../stores/recommendations'
  import { useRecipeStore }          from '../stores/recipe'
  import RecipeRow                   from '../components/RecipeRow.vue'
  import CategoryPicker              from '../components/CategoryPicker.vue'
  
  const auth             = useAuthStore()
  const recs             = useRecommendationStore()
  const recipe           = useRecipeStore()
  
  const selectedCategory = ref('')
  
  onMounted(async () => {
    await recs.fetchLanding()
    selectedCategory.value = recs.byCategory.category
  })
  
  // When user changes category, reload list 2
  watch(selectedCategory, async (cat) => {
    if (cat && cat !== recs.byCategory.category) {
      await recs.changeCategory(cat)
    }
  })
  
  function openRecipe(id) {
    recipe.fetchRecipe(id)
  }
  </script>
  
  <style scoped>
  .home-page     { min-height: 100vh; background: #fafafa; }
  
  /* ── Hero ─────────────────────────────────────────────── */
  .hero {
    background:  linear-gradient(135deg, #f6c90e 0%, #ffb700 100%);
    padding:     3rem 2rem;
  }
  .hero-content  { max-width: 1200px; margin: 0 auto; }
  .hero-content h1 {
    font-size:   2rem;
    font-weight: 800;
    margin:      0 0 0.5rem;
    color:       #3d2c00;
  }
  .hero-name     { color: #fff; }
  .hero-content p { color: #5a3e00; margin: 0 0 1.5rem; font-size: 1.05rem; }
  .btn-search-hero {
    display:       inline-block;
    background:    #fff;
    color:         #5a3e00;
    font-weight:   700;
    border-radius: 10px;
    padding:       0.75rem 1.5rem;
    text-decoration: none;
    transition:    box-shadow 0.15s;
  }
  .btn-search-hero:hover { box-shadow: 0 4px 16px rgba(0,0,0,0.15); }
  
  /* ── Content ──────────────────────────────────────────── */
  .home-content  { max-width: 1200px; margin: 0 auto; padding: 2.5rem 1.5rem; }
  
  .btn-refresh {
    background:    #f0f0f0;
    border:        none;
    border-radius: 8px;
    padding:       0.4rem 0.85rem;
    font-size:     0.82rem;
    cursor:        pointer;
    white-space:   nowrap;
  }
  .btn-refresh:hover { background: #e0e0e0; }
  </style>