<template>
    <Teleport to="body">
      <Transition name="modal-fade">
        <div
          v-if="recipe.selectedRecipe || recipe.loading"
          class="modal-backdrop"
          @click.self="recipe.closeRecipe()"
        >
          <div class="modal" role="dialog" aria-modal="true">
  
            <!-- Header -->
            <div class="modal-header">
              <button class="btn-close" @click="recipe.closeRecipe()" aria-label="Close">✕</button>
            </div>
  
            <!-- Loading state -->
            <div v-if="recipe.loading" class="modal-loading">
              <div class="spinner" />
              <p>Loading recipe...</p>
            </div>
  
            <!-- Content -->
            <template v-else-if="recipe.selectedRecipe">
              <div class="modal-hero">
                <img
                  v-if="recipe.selectedRecipe.image_url"
                  :src="recipe.selectedRecipe.image_url"
                  :alt="recipe.selectedRecipe.name"
                  class="modal-image"
                />
                <div v-else class="modal-no-image">🍽️</div>
              </div>
  
              <div class="modal-body">
  
                <!-- Title row -->
                <div class="modal-title-row">
                  <h2 class="modal-title">{{ recipe.selectedRecipe.name }}</h2>
                  <!-- Bookmark button — wired in Step 6 -->
                  <button class="btn-bookmark" title="Bookmark this recipe">
                    🔖 Save
                  </button>
                </div>
  
                <!-- Meta pills -->
                <div class="modal-meta">
                  <span v-if="recipe.selectedRecipe.rating" class="meta-pill">
                    ⭐ {{ recipe.selectedRecipe.rating.toFixed(1) }}
                  </span>
                  <span v-if="recipe.selectedRecipe.total_time" class="meta-pill">
                    🕒 {{ recipe.selectedRecipe.total_time }}
                  </span>
                  <span v-if="recipe.selectedRecipe.calories" class="meta-pill">
                    🔥 {{ Math.round(recipe.selectedRecipe.calories) }} kcal
                  </span>
                  <span v-if="recipe.selectedRecipe.category" class="meta-pill category">
                    {{ recipe.selectedRecipe.category }}
                  </span>
                </div>
  
                <!-- Description -->
                <p v-if="recipe.selectedRecipe.description" class="modal-description">
                  {{ recipe.selectedRecipe.description }}
                </p>
  
                <!-- Ingredients -->
                <section class="modal-section">
                  <h3>🧂 Ingredients</h3>
                  <ul class="ingredient-list">
                    <li
                      v-for="(item, i) in recipe.selectedRecipe.ingredients_list"
                      :key="i"
                    >
                      {{ item }}
                    </li>
                  </ul>
                </section>
  
                <!-- Instructions -->
                <section class="modal-section">
                  <h3>👨‍🍳 Instructions</h3>
                  <ol class="instruction-list">
                    <li
                      v-for="(step, i) in recipe.selectedRecipe.instructions_list"
                      :key="i"
                      class="instruction-step"
                    >
                      <span class="step-number">{{ i + 1 }}</span>
                      <span class="step-text">{{ step }}</span>
                    </li>
                  </ol>
                </section>
  
                <!-- Keywords -->
                <div v-if="recipe.selectedRecipe.keywords" class="modal-keywords">
                  <span
                    v-for="(kw, i) in keywordList"
                    :key="i"
                    class="keyword-tag"
                  >
                    {{ kw }}
                  </span>
                </div>
  
              </div>
            </template>
  
          </div>
        </div>
      </Transition>
    </Teleport>
  </template>
  
  <script setup>
  import { computed, onMounted, onUnmounted } from 'vue'
  import { useRecipeStore } from '../stores/recipe'
  
  const recipe = useRecipeStore()
  
  // Parse keyword string into array
  const keywordList = computed(() => {
    const kw = recipe.selectedRecipe?.keywords
    if (!kw) return []
    return kw.split(/\s+/).filter(Boolean).slice(0, 10)
  })
  
  // Close modal on Escape key
  function onKeydown(e) {
    if (e.key === 'Escape') recipe.closeRecipe()
  }
  
  // Lock body scroll when modal is open
  onMounted(()  => {
    window.addEventListener('keydown', onKeydown)
    document.body.style.overflow = 'hidden'
  })
  onUnmounted(() => {
    window.removeEventListener('keydown', onKeydown)
    document.body.style.overflow = ''
  })
  </script>
  
  <style scoped>
  /* ── Backdrop ─────────────────────────────────────────── */
  .modal-backdrop {
    position:        fixed;
    inset:           0;
    background:      rgba(0, 0, 0, 0.55);
    display:         flex;
    align-items:     center;
    justify-content: center;
    z-index:         1000;
    padding:         1rem;
  }
  
  /* ── Modal box ────────────────────────────────────────── */
  .modal {
    background:    #fff;
    border-radius: 16px;
    width:         100%;
    max-width:     720px;
    max-height:    90vh;
    overflow-y:    auto;
    position:      relative;
    box-shadow:    0 20px 60px rgba(0,0,0,0.25);
  }
  
  /* ── Header / close button ────────────────────────────── */
  .modal-header {
    position:   sticky;
    top:        0;
    z-index:    10;
    display:    flex;
    justify-content: flex-end;
    padding:    0.75rem 1rem 0;
    background: #fff;
  }
  .btn-close {
    background: #f0f0f0;
    border:     none;
    border-radius: 50%;
    width:  2rem;
    height: 2rem;
    cursor: pointer;
    font-size: 0.9rem;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .btn-close:hover { background: #e0e0e0; }
  
  /* ── Hero image ───────────────────────────────────────── */
  .modal-hero       { width: 100%; height: 280px; overflow: hidden; }
  .modal-image      { width: 100%; height: 100%; object-fit: cover; }
  .modal-no-image   {
    height: 100%; background: #f9f9f9;
    display: flex; align-items: center;
    justify-content: center; font-size: 4rem;
  }
  
  /* ── Body ─────────────────────────────────────────────── */
  .modal-body       { padding: 1.5rem; }
  
  .modal-title-row  {
    display:         flex;
    justify-content: space-between;
    align-items:     flex-start;
    gap:             1rem;
    margin-bottom:   0.75rem;
  }
  .modal-title      { font-size: 1.5rem; font-weight: 700; margin: 0; }
  
  .btn-bookmark {
    flex-shrink:   0;
    background:    #f6c90e;
    border:        none;
    border-radius: 8px;
    padding:       0.5rem 1rem;
    font-weight:   600;
    cursor:        pointer;
    white-space:   nowrap;
  }
  .btn-bookmark:hover { background: #e0b800; }
  
  /* ── Meta pills ───────────────────────────────────────── */
  .modal-meta       { display: flex; flex-wrap: wrap; gap: 0.5rem; margin-bottom: 1rem; }
  .meta-pill {
    background:    #f5f5f5;
    border-radius: 20px;
    padding:       0.3rem 0.75rem;
    font-size:     0.85rem;
    color:         #555;
  }
  .meta-pill.category { background: #f6c90e22; color: #92620a; }
  
  /* ── Description ──────────────────────────────────────── */
  .modal-description {
    color:         #555;
    line-height:   1.6;
    margin-bottom: 1.5rem;
    font-size:     0.95rem;
  }
  
  /* ── Sections ─────────────────────────────────────────── */
  .modal-section    { margin-bottom: 1.75rem; }
  .modal-section h3 { font-size: 1.1rem; margin-bottom: 0.75rem; }
  
  /* ── Ingredients ──────────────────────────────────────── */
  .ingredient-list  {
    list-style: none;
    padding:    0;
    display:    grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap:        0.4rem;
  }
  .ingredient-list li {
    padding:       0.4rem 0.6rem;
    background:    #f9f9f9;
    border-radius: 6px;
    font-size:     0.9rem;
  }
  .ingredient-list li::before { content: '• '; color: #f6c90e; }
  
  /* ── Instructions ─────────────────────────────────────── */
  .instruction-list { list-style: none; padding: 0; }
  .instruction-step {
    display:       flex;
    gap:           1rem;
    margin-bottom: 1rem;
    align-items:   flex-start;
  }
  .step-number {
    flex-shrink:     0;
    width:           2rem;
    height:          2rem;
    background:      #f6c90e;
    border-radius:   50%;
    display:         flex;
    align-items:     center;
    justify-content: center;
    font-weight:     700;
    font-size:       0.85rem;
  }
  .step-text { line-height: 1.6; font-size: 0.95rem; padding-top: 0.2rem; }
  
  /* ── Keywords ─────────────────────────────────────────── */
  .modal-keywords   { display: flex; flex-wrap: wrap; gap: 0.4rem; margin-top: 1rem; }
  .keyword-tag {
    background:    #f0f0f0;
    border-radius: 4px;
    padding:       0.2rem 0.6rem;
    font-size:     0.78rem;
    color:         #666;
  }
  
  /* ── Loading spinner ──────────────────────────────────── */
  .modal-loading {
    display:         flex;
    flex-direction:  column;
    align-items:     center;
    justify-content: center;
    padding:         4rem;
    gap:             1rem;
    color:           #888;
  }
  .spinner {
    width:  2.5rem;
    height: 2.5rem;
    border: 3px solid #f0f0f0;
    border-top-color: #f6c90e;
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
  }
  @keyframes spin { to { transform: rotate(360deg); } }
  
  /* ── Transition ───────────────────────────────────────── */
  .modal-fade-enter-active,
  .modal-fade-leave-active { transition: opacity 0.2s ease; }
  .modal-fade-enter-from,
  .modal-fade-leave-to    { opacity: 0; }
  </style>