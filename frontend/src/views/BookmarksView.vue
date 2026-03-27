<template>
    <div class="bookmarks-page">
        <div class="page-layout">

            <!-- Left: Folder manager sidebar -->
            <aside class="sidebar">
                <FolderManager :selected-id="activeFolderId" @select="selectFolder" />
            </aside>

            <!-- Right: Bookmark list -->
            <main class="bookmark-main">
                <div class="bookmark-header">
                    <h2>
                        {{ activeFolderName || 'All Bookmarks' }}
                        <span class="count">({{ displayedBookmarks.length }})</span>
                    </h2>
                    <div class="sort-row">
                        <label>Sort by</label>
                        <select v-model="sortBy">
                            <option value="rating">Rating</option>
                            <option value="newest">Newest</option>
                        </select>
                    </div>
                </div>

                <div v-if="bookmarks.loading" class="bm-loading">
                    Loading bookmarks...
                </div>

                <div v-else-if="displayedBookmarks.length === 0" class="bm-empty">
                    <p>No bookmarks here yet.</p>
                    <router-link to="/search">Search for recipes →</router-link>
                </div>

                <div v-else class="bookmark-grid">
                    <div v-for="bm in sortedBookmarks" :key="bm.id" class="bookmark-card">
                        <div class="bm-image" @click="openRecipe(bm.recipe_id)">
                            <LazyImage :src="bm.recipe?.image_url" :alt="bm.recipe?.name" aspect-ratio="4/3" />
                        </div>

                        <div class="bm-body">
                            <h4 class="bm-title" @click="openRecipe(bm.recipe_id)">
                                {{ bm.recipe?.name }}
                            </h4>

                            <StarRating :model-value="bm.rating" readonly />

                            <div class="bm-meta">
                                <span v-if="bm.recipe?.total_time">🕒 {{ bm.recipe.total_time }}</span>
                                <span v-if="bm.recipe?.category">{{ bm.recipe.category }}</span>
                            </div>
                        </div>

                        <button class="bm-remove" title="Remove bookmark" @click="removeBookmark(bm.id)">
                            🗑
                        </button>
                    </div>
                </div>
                <FolderSuggestions v-if="activeFolderId" :suggestions="recommendations.suggestions"
                    :loading="recommendations.suggestLoading" @refresh="loadSuggestions" @select="openRecipe" />
            </main>
        </div>
    </div>
</template>
  
<script setup>
import { ref, computed, onMounted } from 'vue'
import { useBookmarkStore } from '../stores/bookmark'
import { useRecipeStore } from '../stores/recipe'
import FolderManager from '../components/FolderManager.vue'
import StarRating from '../components/StarRating.vue'
import { useRecommendationStore } from '../stores/recommendations'
import FolderSuggestions from '../components/FolderSuggestions.vue'
import LazyImage from '../components/LazyImage.vue'

const bookmarks = useBookmarkStore()
const recipe = useRecipeStore()
const recommendations = useRecommendationStore()

const activeFolderId = ref(null)
const activeFolderName = ref('')
const sortBy = ref('rating')

onMounted(() => bookmarks.fetchAll())

const displayedBookmarks = computed(() =>
    activeFolderId.value
        ? bookmarks.folderBookmarks
        : bookmarks.allBookmarks
)

const sortedBookmarks = computed(() => {
    const list = [...displayedBookmarks.value]
    if (sortBy.value === 'rating') {
        return list.sort((a, b) => b.rating - a.rating)
    }
    return list.sort((a, b) => b.id - a.id)   // newest by id
})

async function selectFolder(folder) {
    activeFolderId.value = folder.id
    activeFolderName.value = folder.name
    await bookmarks.fetchByFolder(folder.id)
    await recommendations.fetchFolderSuggestions(folder.id)   // ← add this
}

async function loadSuggestions() {
    if (activeFolderId.value) {
        await recommendations.fetchFolderSuggestions(activeFolderId.value)
    }
}

async function removeBookmark(id) {
    if (confirm('Remove this bookmark?')) {
        await bookmarks.removeBookmark(id)
    }
}

function openRecipe(id) {
    recipe.fetchRecipe(id)
}
</script>
  
<style scoped>
.bookmarks-page {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem 1rem;
}

.page-layout {
    display: grid;
    grid-template-columns: 280px 1fr;
    gap: 1.5rem;
}

@media (max-width: 700px) {
    .page-layout {
        grid-template-columns: 1fr;
    }
}

.bookmark-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1.25rem;
}

.bookmark-header h2 {
    margin: 0;
    font-size: 1.2rem;
}

.count {
    color: #aaa;
    font-size: 0.9rem;
    font-weight: 400;
}

.sort-row {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.85rem;
}

.sort-row select {
    padding: 0.3rem 0.5rem;
    border: 1px solid #ddd;
    border-radius: 6px;
}

.bookmark-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 1rem;
}

.bookmark-card {
    border: 1px solid #eee;
    border-radius: 12px;
    overflow: hidden;
    background: #fff;
    position: relative;
}

.bm-image {
    height: 140px;
    overflow: hidden;
    cursor: pointer;
    background: #f5f5f5;
}

.bm-image img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.bm-no-image {
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2.5rem;
}

.bm-body {
    padding: 0.75rem;
}

.bm-title {
    font-size: 0.9rem;
    font-weight: 600;
    margin: 0 0 0.35rem;
    cursor: pointer;
}

.bm-title:hover {
    color: #d97706;
}

.bm-meta {
    display: flex;
    gap: 0.5rem;
    font-size: 0.75rem;
    color: #888;
    margin-top: 0.35rem;
    flex-wrap: wrap;
}

.bm-remove {
    position: absolute;
    top: 0.5rem;
    right: 0.5rem;
    background: rgba(255, 255, 255, 0.85);
    border: none;
    border-radius: 6px;
    padding: 0.2rem 0.4rem;
    cursor: pointer;
    opacity: 0;
    transition: opacity 0.15s;
}

.bookmark-card:hover .bm-remove {
    opacity: 1;
}

.bm-loading,
.bm-empty {
    color: #aaa;
    text-align: center;
    padding: 3rem 0;
}

.bm-empty a {
    color: #d97706;
}
</style>