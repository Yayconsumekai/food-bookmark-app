<template>
    <div class="category-picker">
      <label class="picker-label">Browse Category</label>
      <div class="picker-scroll">
        <button
          v-for="cat in categories"
          :key="cat"
          class="cat-pill"
          :class="{ active: modelValue === cat }"
          @click="$emit('update:modelValue', cat)"
        >
          {{ cat }}
        </button>
      </div>
    </div>
  </template>
  
  <script setup>
  defineProps({
    categories: { type: Array,  default: () => [] },
    modelValue: { type: String, default: '' },
  })
  defineEmits(['update:modelValue'])
  </script>
  
  <style scoped>
  .category-picker  { margin-bottom: 0.5rem; }
  .picker-label     { font-size: 0.8rem; color: #888; display: block; margin-bottom: 0.5rem; }
  .picker-scroll    {
    display:          flex;
    gap:              0.5rem;
    overflow-x:       auto;
    padding-bottom:   0.25rem;
    scrollbar-width:  none;
  }
  .picker-scroll::-webkit-scrollbar { display: none; }
  .cat-pill {
    flex-shrink:   0;
    background:    #f0f0f0;
    border:        2px solid transparent;
    border-radius: 20px;
    padding:       0.3rem 0.85rem;
    font-size:     0.82rem;
    cursor:        pointer;
    white-space:   nowrap;
    transition:    all 0.15s;
  }
  .cat-pill:hover  { background: #ffe8a0; }
  .cat-pill.active {
    background:   #f6c90e;
    border-color: #d4a800;
    font-weight:  600;
  }
  </style>