<template>
    <div class="folder-suggestions">
        <div class="suggest-header">
            <div>
                <h3 class="suggest-title">✨ Suggested for this Folder</h3>
                <p class="suggest-subtitle">
                    Powered by TF-IDF cosine similarity — recipes similar to what's in this folder
                </p>
            </div>
            <button class="btn-refresh" @click="$emit('refresh')" :disabled="loading">
                {{ loading ? '⏳ Loading...' : '🔄 Refresh' }}
            </button>
        </div>

        <!-- Loading -->
        <div v-if="loading" class="row-scroll">
            <div v-for="n in 6" :key="n" class="skeleton-card" />
        </div>

        <!-- Empty -->
        <div v-else-if="!suggestions.length" class="suggest-empty">
            No suggestions yet — add more recipes to this folder to improve results.
        </div>

        <!-- Suggestion cards -->
        <div v-else class="row-scroll">
            <div v-for="recipe in suggestions" :key="recipe.id" class="suggest-card" @click="$emit('select', recipe.id)">
                <div class="card-img">
                    <LazyImage :src="recipe.image_url" :alt="recipe.name" aspect-ratio="3/2" />
                    <span class="match-badge">
                        {{ Math.round(recipe.similarity * 100) }}% match
                    </span>
                </div>
                <div class="card-info">
                    <p class="card-name">{{ recipe.name }}</p>
                    <div class="card-meta">
                        <span v-if="recipe.rating">⭐ {{ recipe.rating.toFixed(1) }}</span>
                        <span v-if="recipe.category" class="cat-tag">{{ recipe.category }}</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
  
<script setup>
import LazyImage from './LazyImage.vue'

defineProps({
    suggestions: { type: Array, default: () => [] },
    loading: { type: Boolean, default: false },
})
defineEmits(['refresh', 'select'])
</script>
  
<style scoped>
.folder-suggestions {
    margin-top: 2rem;
    padding: 1.25rem;
    background: linear-gradient(135deg, #fffbea, #fff8e1);
    border: 1px solid #f6c90e55;
    border-radius: 14px;
}

.suggest-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 1rem;
    gap: 1rem;
}

.suggest-title {
    font-size: 1rem;
    font-weight: 700;
    margin: 0;
}

.suggest-subtitle {
    font-size: 0.78rem;
    color: #888;
    margin: 0.2rem 0 0;
}

.btn-refresh {
    flex-shrink: 0;
    background: #f6c90e;
    border: none;
    border-radius: 8px;
    padding: 0.4rem 0.85rem;
    font-size: 0.82rem;
    font-weight: 600;
    cursor: pointer;
    white-space: nowrap;
}

.btn-refresh:disabled {
    opacity: 0.6;
    cursor: default;
}

.row-scroll {
    display: grid;
    grid-auto-flow: column;
    grid-auto-columns: 180px;
    gap: 0.85rem;
    overflow-x: auto;
    padding-bottom: 0.5rem;
    scrollbar-width: thin;
}

.suggest-card {
    border: 1px solid #eee;
    border-radius: 10px;
    overflow: hidden;
    background: #fff;
    cursor: pointer;
    transition: transform 0.15s, box-shadow 0.15s;
}

.suggest-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
}

.card-img {
    height: 120px;
    overflow: hidden;
    background: #f5f5f5;
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
    font-size: 2rem;
}

.match-badge {
    position: absolute;
    bottom: 0.3rem;
    right: 0.3rem;
    background: rgba(246, 201, 14, 0.92);
    border-radius: 5px;
    padding: 0.1rem 0.4rem;
    font-size: 0.7rem;
    font-weight: 700;
    color: #5a3e00;
}

.card-info {
    padding: 0.55rem;
}

.card-name {
    font-size: 0.82rem;
    font-weight: 600;
    margin: 0 0 0.25rem;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

.card-meta {
    display: flex;
    gap: 0.4rem;
    font-size: 0.72rem;
    color: #888;
    flex-wrap: wrap;
}

.cat-tag {
    background: #f0f0f0;
    border-radius: 4px;
    padding: 0.1rem 0.35rem;
}

.suggest-empty {
    color: #aaa;
    font-size: 0.85rem;
    padding: 1rem 0;
    text-align: center;
}

.skeleton-card {
    width: 180px;
    height: 190px;
    flex-shrink: 0;
    border-radius: 10px;
    background: linear-gradient(90deg, #f5f0d8 25%, #ede8cc 50%, #f5f0d8 75%);
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
}</style>