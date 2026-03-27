import { defineStore } from 'pinia'
import api from '../api/index.js'

export const useRecommendationStore = defineStore('recommendations', {
  state: () => ({
    forYou:       [],
    byCategory:   { category: '', recipes: [] },
    discover:     [],
    categories:   [],
    suggestions:  [],    // ML folder suggestions
    loading:      false,
    suggestLoading: false,
    error:        null,
  }),

  actions: {
    async fetchLanding(category = null) {
      this.loading = true
      this.error   = null
      try {
        const params = category ? { category } : {}
        const { data } = await api.get('/api/recommendations/landing', { params })
        this.forYou     = data.for_you
        this.byCategory = data.by_category
        this.discover   = data.discover
        this.categories = data.categories
      } catch (e) {
        this.error = e.response?.data?.detail || 'Failed to load recommendations'
      } finally {
        this.loading = false
      }
    },

    async fetchFolderSuggestions(folderId) {
      this.suggestLoading = true
      this.suggestions    = []
      try {
        const { data } = await api.get(`/api/recommendations/folder/${folderId}`)
        this.suggestions = data.suggestions
      } finally {
        this.suggestLoading = false
      }
    },

    async changeCategory(category) {
      await this.fetchLanding(category)
    },
  },
})