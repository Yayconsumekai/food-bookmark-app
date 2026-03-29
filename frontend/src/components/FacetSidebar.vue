<template>
    <aside class="facet-sidebar" v-if="facets">
  
      <div class="facet-group">
        <h4 class="facet-title">⭐ Min Rating</h4>
        <div class="facet-options">
          <button
            v-for="opt in ratingOptions"
            :key="opt.value"
            class="facet-btn"
            :class="{ active: filters.minRating === opt.value }"
            @click="toggleRating(opt.value)"
          >
            {{ opt.label }}
            <span class="facet-count" v-if="getRatingCount(opt.label)">
              ({{ getRatingCount(opt.label) }})
            </span>
          </button>
        </div>
      </div>
  
      <div class="facet-group">
        <h4 class="facet-title">🕒 Max Time</h4>
        <div class="facet-options">
          <button
            v-for="opt in timeOptions"
            :key="opt.value"
            class="facet-btn"
            :class="{ active: filters.maxMinutes === opt.value }"
            @click="toggleTime(opt.value)"
          >
            {{ opt.label }}
          </button>
        </div>
      </div>
  
      <div class="facet-group">
        <h4 class="facet-title">🍽️ Category</h4>
        <div class="facet-options">
          <button
            v-for="cat in facets.categories"
            :key="cat.name"
            class="facet-btn"
            :class="{ active: filters.category === cat.name }"
            @click="toggleCategory(cat.name)"
          >
            {{ cat.name }}
            <span class="facet-count">({{ cat.count }})</span>
          </button>
        </div>
      </div>
  
      <button
        v-if="hasActiveFilters"
        class="btn-clear"
        @click="clearAll"
      >
        ✕ Clear all filters
      </button>
  
    </aside>
  </template>
  
  <script setup>
  import { computed } from 'vue'
  
  const props = defineProps({
    facets:  { type: Object, default: null },
    filters: { type: Object, required: true },
  })
  const emit = defineEmits(['update:filters', 'apply'])
  
  const ratingOptions = [
    { label: '4.5+', value: 4.5 },
    { label: '4.0+', value: 4.0 },
    { label: '3.0+', value: 3.0 },
  ]
  
  const timeOptions = [
    { label: '≤ 30 min',  value: 30  },
    { label: '≤ 1 hour',  value: 60  },
    { label: '≤ 2 hours', value: 120 },
  ]
  
  const hasActiveFilters = computed(() =>
    props.filters.category  !== null ||
    props.filters.minRating !== null ||
    props.filters.maxMinutes !== null
  )
  
  function getRatingCount(label) {
    const match = props.facets?.ratings?.find(r => r.band === label)
    return match?.count || null
  }
  
  function toggleRating(value) {
    const next = props.filters.minRating === value ? null : value
    emit('update:filters', { ...props.filters, minRating: next })
    emit('apply')
  }
  
  function toggleTime(value) {
    const next = props.filters.maxMinutes === value ? null : value
    emit('update:filters', { ...props.filters, maxMinutes: next })
    emit('apply')
  }
  
  function toggleCategory(name) {
    const next = props.filters.category === name ? null : name
    emit('update:filters', { ...props.filters, category: next })
    emit('apply')
  }
  
  function clearAll() {
    emit('update:filters', { category: null, minRating: null, maxMinutes: null })
    emit('apply')
  }
  </script>
  
  <style scoped>
  .facet-sidebar    {
    width:         220px;
    flex-shrink:   0;
    background:    #fff;
    border:        1px solid #eee;
    border-radius: 12px;
    padding:       1.25rem;
    align-self:    start;
    position:      sticky;
    top:           80px;
  }
  .facet-group      { margin-bottom: 1.25rem; }
  .facet-title      { font-size: 0.85rem; font-weight: 700;
                      margin: 0 0 0.6rem; color: #333; }
  .facet-options    { display: flex; flex-direction: column; gap: 0.3rem; }
  .facet-btn {
    text-align:    left;
    background:    #f9f9f9;
    border:        2px solid transparent;
    border-radius: 8px;
    padding:       0.35rem 0.65rem;
    font-size:     0.82rem;
    cursor:        pointer;
    display:       flex;
    justify-content: space-between;
    align-items:   center;
    transition:    all 0.12s;
  }
  .facet-btn:hover  { background: #f0f0f0; }
  .facet-btn.active {
    border-color:  #f6c90e;
    background:    #fffbea;
    font-weight:   600;
  }
  .facet-count      { color: #aaa; font-size: 0.75rem; }
  .btn-clear {
    width:         100%;
    background:    none;
    border:        1px solid #fca5a5;
    border-radius: 8px;
    color:         #ef4444;
    padding:       0.4rem;
    cursor:        pointer;
    font-size:     0.82rem;
    margin-top:    0.5rem;
  }
  .btn-clear:hover { background: #fee2e2; }
  </style>