<template>
    <div v-if="search.pendingCorrection" class="spell-banner">
      <span class="spell-icon">✏️</span>
      <span class="spell-text">
        Did you mean
        <strong class="corrected-query">{{ search.spellResult.corrected }}</strong>
        ?
      </span>
      <div class="spell-actions">
        <button class="btn-accept" @click="search.acceptCorrection()">
          Yes, search for "{{ search.spellResult.corrected }}"
        </button>
        <button class="btn-reject" @click="search.rejectCorrection()">
          No, keep "{{ search.spellResult.original }}"
        </button>
      </div>
    </div>
  </template>
  
  <script setup>
  import { useSearchStore } from '../stores/search'
  const search = useSearchStore()
  </script>
  
  <style scoped>
  .spell-banner {
    display:          flex;
    align-items:      center;
    flex-wrap:        wrap;
    gap:              0.75rem;
    background:       #fffbea;
    border:           1px solid #f6c90e;
    border-radius:    8px;
    padding:          0.75rem 1rem;
    margin:           0.5rem 0;
    font-size:        0.95rem;
  }
  .corrected-query { color: #d97706; }
  .btn-accept {
    background: #f6c90e; border: none;
    border-radius: 6px; padding: 0.4rem 0.9rem;
    cursor: pointer; font-weight: 600;
  }
  .btn-reject {
    background: transparent; border: 1px solid #aaa;
    border-radius: 6px; padding: 0.4rem 0.9rem;
    cursor: pointer; color: #666;
  }
  </style>