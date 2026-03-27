<template>
    <div class="lazy-wrapper" :style="{ aspectRatio }">
  
      <!-- Blur placeholder shown until image loads -->
      <div
        class="lazy-placeholder"
        :class="{ hidden: loaded || error }"
      />
  
      <!-- Actual image -->
      <img
        v-if="!error"
        ref="imgRef"
        :src="proxiedSrc"
        :alt="alt"
        class="lazy-img"
        :class="{ visible: loaded }"
        loading="lazy"
        decoding="async"
        @load="onLoad"
        @error="onError"
      />
  
      <!-- Fallback if image fails -->
      <div v-if="error" class="lazy-fallback">
        {{ fallback }}
      </div>
  
    </div>
  </template>
  
  <script setup>
  import { ref, computed } from 'vue'
  
  const props = defineProps({
    src:         { type: String, default: '' },
    alt:         { type: String, default: '' },
    fallback:    { type: String, default: '🍽️' },
    aspectRatio: { type: String, default: '4/3' },
    proxy:       { type: Boolean, default: true },   // use backend proxy
  })
  
  const loaded  = ref(false)
  const error   = ref(false)
  const imgRef  = ref(null)
  
  // Route through our image proxy for on-demand caching
  const proxiedSrc = computed(() => {
    if (!props.src || !props.proxy) return props.src
    // If already a local static URL, serve directly
    if (props.src.includes('/static/images/')) return props.src
    // Otherwise proxy through backend
    return `http://localhost:8000/api/search/image-proxy?url=${encodeURIComponent(props.src)}`
  })
  
  function onLoad()  { loaded.value = true  }
  function onError() { error.value  = true  }
  </script>
  
  <style scoped>
  .lazy-wrapper {
    position:   relative;
    overflow:   hidden;
    background: #f5f5f5;
    width:      100%;
  }
  
  /* Animated shimmer placeholder */
  .lazy-placeholder {
    position:        absolute;
    inset:           0;
    background:      linear-gradient(
      90deg,
      #f0f0f0 25%,
      #e4e4e4 50%,
      #f0f0f0 75%
    );
    background-size: 200% 100%;
    animation:       shimmer 1.4s infinite;
    transition:      opacity 0.3s;
  }
  .lazy-placeholder.hidden { opacity: 0; pointer-events: none; }
  
  @keyframes shimmer {
    0%   { background-position:  200% 0; }
    100% { background-position: -200% 0; }
  }
  
  /* Image starts invisible, fades in on load */
  .lazy-img {
    position:   absolute;
    inset:      0;
    width:      100%;
    height:     100%;
    object-fit: cover;
    opacity:    0;
    transition: opacity 0.35s ease;
  }
  .lazy-img.visible { opacity: 1; }
  
  /* Fallback emoji */
  .lazy-fallback {
    position:        absolute;
    inset:           0;
    display:         flex;
    align-items:     center;
    justify-content: center;
    font-size:       2.5rem;
    background:      #f9f9f9;
  }
  </style>