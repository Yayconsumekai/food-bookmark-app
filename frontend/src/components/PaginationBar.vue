<template>
    <div class="pagination" v-if="totalPages > 1">
  
      <!-- Previous -->
      <button
        class="page-btn"
        :disabled="currentPage === 1"
        @click="$emit('go', currentPage - 1)"
      >
        ← Prev
      </button>
  
      <!-- Page numbers -->
      <template v-for="page in visiblePages" :key="page">
        <!-- Ellipsis -->
        <span v-if="page === '...'" class="ellipsis">…</span>
  
        <!-- Page button -->
        <button
          v-else
          class="page-btn"
          :class="{ active: page === currentPage }"
          @click="$emit('go', page)"
        >
          {{ page }}
        </button>
      </template>
  
      <!-- Next -->
      <button
        class="page-btn"
        :disabled="currentPage === totalPages"
        @click="$emit('go', currentPage + 1)"
      >
        Next →
      </button>
  
    </div>
  </template>
  
  <script setup>
  import { computed } from 'vue'
  
  const props = defineProps({
    currentPage: { type: Number, required: true },
    totalPages:  { type: Number, required: true },
  })
  defineEmits(['go'])
  
  // Show: first, last, current ±2, with ellipsis in between
  const visiblePages = computed(() => {
    const pages = []
    const total = props.totalPages
    const cur   = props.currentPage
    const delta = 2   // pages on each side of current
  
    const range     = []
    const rangeSet  = new Set()
  
    // Always include first and last
    const addPage = (p) => {
      if (p >= 1 && p <= total && !rangeSet.has(p)) {
        range.push(p)
        rangeSet.add(p)
      }
    }
  
    addPage(1)
    addPage(total)
    for (let i = cur - delta; i <= cur + delta; i++) addPage(i)
  
    range.sort((a, b) => a - b)
  
    // Insert ellipsis where there are gaps
    for (let i = 0; i < range.length; i++) {
      if (i > 0 && range[i] - range[i - 1] > 1) {
        pages.push('...')
      }
      pages.push(range[i])
    }
  
    return pages
  })
  </script>
  
  <style scoped>
  .pagination {
    display:         flex;
    justify-content: center;
    align-items:     center;
    gap:             0.4rem;
    margin-top:      2rem;
    flex-wrap:       wrap;
  }
  .page-btn {
    min-width:     2.2rem;
    height:        2.2rem;
    padding:       0 0.6rem;
    border:        1px solid #ddd;
    border-radius: 8px;
    background:    #fff;
    cursor:        pointer;
    font-size:     0.88rem;
    transition:    all 0.12s;
  }
  .page-btn:hover:not(:disabled) {
    background:    #f6c90e;
    border-color:  #d4a800;
  }
  .page-btn.active {
    background:    #f6c90e;
    border-color:  #d4a800;
    font-weight:   700;
  }
  .page-btn:disabled {
    opacity:  0.4;
    cursor:   default;
  }
  .ellipsis {
    color:      #aaa;
    padding:    0 0.25rem;
    font-size:  0.9rem;
  }
  </style>