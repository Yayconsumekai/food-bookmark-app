<template>
    <div v-if="expansion" class="expansion-banner">
      <span class="expansion-icon">🔍</span>
      <span class="expansion-text">
        Search expanded with synonyms:
        <span
          v-for="(synonyms, word) in expansion.expansions_used"
          :key="word"
          class="expansion-item"
        >
          <strong>{{ word }}</strong>
          → {{ synonyms.join(', ') }}
        </span>
      </span>
    </div>
  </template>
  
  <script setup>
  defineProps({
    expansion: { type: Object, default: null }
  })
  </script>
  
  <style scoped>
  .expansion-banner {
    display:       flex;
    align-items:   center;
    flex-wrap:     wrap;
    gap:           0.5rem;
    background:    #f0fdf4;
    border:        1px solid #86efac;
    border-radius: 8px;
    padding:       0.6rem 1rem;
    font-size:     0.85rem;
    margin:        0.5rem 0;
  }
  .expansion-icon  { font-size: 1rem; }
  .expansion-item  { margin-left: 0.5rem; }
  .expansion-item strong { color: #16a34a; }
  </style>