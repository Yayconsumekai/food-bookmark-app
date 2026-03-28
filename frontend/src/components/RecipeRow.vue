<template>
    <section class="recipe-row">
        <div class="row-header">
            <div class="row-title-group">
                <h2 class="row-title">{{ title }}</h2>
                <p v-if="subtitle" class="row-subtitle">{{ subtitle }}</p>
            </div>
            <slot name="header-action" />
        </div>

        <!-- Loading skeleton -->
        <div v-if="loading" class="row-scroll">
            <div v-for="n in 5" :key="n" class="skeleton-card" />
        </div>

        <!-- Empty -->
        <div v-else-if="!recipes.length" class="row-empty">
            {{ emptyText }}
        </div>

        <!-- Cards -->
        <div v-else class="row-scroll">
            <div v-for="recipe in recipes.filter(r => r.image_url)" :key="recipe.id" class="row-card"
                @click="$emit('select', recipe.id)">
                <div class="card-img">
                    <LazyImage :src="recipe.image_url" :alt="recipe.name" aspect-ratio="3/2" />
                    <span v-if="recipe.similarity" class="similarity-badge">
                        {{ Math.round(recipe.similarity * 100) }}% match
                    </span>
                </div>

                <div class="card-info">
                    <p class="card-name">{{ recipe.name }}</p>
                    <div class="card-meta">
                        <span v-if="recipe.rating">⭐ {{ recipe.rating.toFixed(1) }}</span>
                        <span v-if="recipe.total_time">🕒 {{ recipe.total_time }}</span>
                    </div>
                </div>
            </div>
        </div>
    </section>
</template>
  
<script setup>
import LazyImage from './LazyImage.vue'

defineProps({
    title: { type: String, required: true },
    subtitle: { type: String, default: '' },
    recipes: { type: Array, default: () => [] },
    loading: { type: Boolean, default: false },
    emptyText: { type: String, default: 'Nothing here yet.' },
})
defineEmits(['select'])
</script>
  
<style scoped>
.recipe-row {
    margin-bottom: 2.5rem;
}

.row-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    margin-bottom: 1rem;
}

.row-title {
    font-size: 1.25rem;
    font-weight: 700;
    margin: 0;
}

.row-subtitle {
    font-size: 0.85rem;
    color: #888;
    margin: 0.2rem 0 0;
}

/* Horizontal scroll container */
.row-scroll {
    display: grid;
    grid-auto-flow: column;
    grid-auto-columns: 200px;
    gap: 1rem;
    overflow-x: auto;
    padding-bottom: 0.75rem;
    scrollbar-width: thin;
    scrollbar-color: #e0e0e0 transparent;
}

.row-scroll::-webkit-scrollbar {
    height: 4px;
}

.row-scroll::-webkit-scrollbar-thumb {
    background: #e0e0e0;
    border-radius: 4px;
}

/* Individual card */
.row-card {
    border: 1px solid #eee;
    border-radius: 12px;
    overflow: hidden;
    background: #fff;
    cursor: pointer;
    transition: transform 0.15s, box-shadow 0.15s;
    flex-shrink: 0;
}

.row-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1);
}

.card-img {
    overflow: hidden;
    position: relative;
}

.card-img img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.card-no-img {
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2.5rem;
}

/* ML similarity badge */
.similarity-badge {
    position: absolute;
    bottom: 0.4rem;
    right: 0.4rem;
    background: rgba(246, 201, 14, 0.92);
    border-radius: 6px;
    padding: 0.15rem 0.45rem;
    font-size: 0.72rem;
    font-weight: 700;
    color: #5a3e00;
}

.card-info {
    padding: 0.65rem;
}

.card-name {
    font-size: 0.85rem;
    font-weight: 600;
    margin: 0 0 0.3rem;
    line-height: 1.3;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

.card-meta {
    display: flex;
    gap: 0.5rem;
    font-size: 0.75rem;
    color: #888;
    flex-wrap: wrap;
}

/* Skeleton */
.skeleton-card {
    width: 200px;
    height: 200px;
    flex-shrink: 0;
    border-radius: 12px;
    background: linear-gradient(90deg, #f0f0f0 25%, #e8e8e8 50%, #f0f0f0 75%);
    background-size: 200% 100%;
    animation: shimmer 1.4s infinite;
}

@keyframes shimmer {
    0% {
        background-position: 200% 0;
    }

    100% {
        background-position: -200% 0;
    }
}

.row-empty {
    color: #aaa;
    font-size: 0.9rem;
    padding: 1rem 0;
}
</style>