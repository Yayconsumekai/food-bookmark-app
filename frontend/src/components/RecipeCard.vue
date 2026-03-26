<template>
    <div class="recipe-card" @click="$emit('select', recipe)">
      <div class="card-image">
        <img
          v-if="recipe.image_url"
          :src="recipe.image_url"
          :alt="recipe.name"
          loading="lazy"
        />
        <div v-else class="no-image">🍽️</div>
      </div>
      <div class="card-body">
        <h3 class="card-title">{{ recipe.name }}</h3>
        <div class="card-meta">
          <span v-if="recipe.rating">⭐ {{ recipe.rating.toFixed(1) }}</span>
          <span v-if="recipe.total_time">🕒 {{ recipe.total_time }}</span>
          <span v-if="recipe.category" class="card-category">{{ recipe.category }}</span>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  defineProps({ recipe: Object })
  defineEmits(['select'])
  </script>
  
  <style scoped>
  .recipe-card {
    border:         1px solid #eee;
    border-radius:  12px;
    overflow:       hidden;
    cursor:         pointer;
    transition:     transform 0.15s, box-shadow 0.15s;
    background:     #fff;
  }
  .recipe-card:hover {
    transform:      translateY(-3px);
    box-shadow:     0 6px 20px rgba(0,0,0,0.1);
  }
  .card-image { height: 180px; overflow: hidden; background: #f5f5f5; }
  .card-image img { width: 100%; height: 100%; object-fit: cover; }
  .no-image {
    height: 100%; display: flex;
    align-items: center; justify-content: center;
    font-size: 3rem;
  }
  .card-body { padding: 0.85rem; }
  .card-title { font-size: 1rem; font-weight: 600; margin: 0 0 0.4rem; }
  .card-meta {
    display: flex; gap: 0.6rem;
    font-size: 0.8rem; color: #666; flex-wrap: wrap;
  }
  .card-category {
    background: #f6c90e22; color: #92620a;
    border-radius: 4px; padding: 0.1rem 0.4rem;
  }
  </style>