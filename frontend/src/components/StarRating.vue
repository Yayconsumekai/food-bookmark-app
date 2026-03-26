<template>
    <div class="star-rating" :class="{ readonly }">
      <button
        v-for="n in 5"
        :key="n"
        class="star"
        :class="{ filled: n <= hovered || (!hovered && n <= modelValue) }"
        @mouseenter="!readonly && (hovered = n)"
        @mouseleave="!readonly && (hovered = 0)"
        @click="!readonly && $emit('update:modelValue', n)"
        :disabled="readonly"
        :aria-label="`Rate ${n} stars`"
      >
        ★
      </button>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  
  defineProps({
    modelValue: { type: Number, default: 0 },
    readonly:   { type: Boolean, default: false },
  })
  defineEmits(['update:modelValue'])
  
  const hovered = ref(0)
  </script>
  
  <style scoped>
  .star-rating { display: inline-flex; gap: 0.15rem; }
  .star {
    background: none; border: none;
    font-size:  1.5rem;
    color:      #ddd;
    cursor:     pointer;
    padding:    0;
    transition: color 0.1s;
    line-height: 1;
  }
  .star.filled        { color: #f6c90e; }
  .readonly .star     { cursor: default; }
  </style>