import { defineStore } from 'pinia'
import api from '../api/index.js'

export const useSearchStore = defineStore('search', {
  state: () => ({
    query:             '',
    results:           [],
    total:             0,
    facets:            null,    // ← add
    loading:           false,
    error:             null,
    expansion:         null,
    spellResult:       null,
    pendingCorrection: false,
  }),

  actions: {
    async search(q, offset = 0) {
      this.loading   = true
      this.error     = null
      this.expansion = null
      try {
        const { data } = await api.get('/api/search/', {
          params: { q, limit: 20, offset }
        })
        this.results   = data.results
        this.total     = data.total
        this.expansion = data.expansion
        this.facets    = data.facets    // ← add
        this.query     = q
      } catch (e) {
        this.error = e.response?.data?.detail || 'Search failed'
      } finally {
        this.loading = false
      }
    },

    async checkSpelling(q) {
      try {
        const { data } = await api.get('/api/search/spell-check', { params: { q } })
        this.spellResult = data
        this.pendingCorrection = data.has_corrections
        return data
      } catch {
        return null
      }
    },

    async searchWithFilters(q, filters = {}) {
      this.loading = true
      this.error   = null
      try {
        const params = {
          q,
          limit: 20,
          offset: 0,
          ...(filters.category   && { category:    filters.category }),
          ...(filters.minRating  && { min_rating:  filters.minRating }),
          ...(filters.maxMinutes && { max_minutes: filters.maxMinutes }),
        }
        const { data } = await api.get('/api/search/', { params })
        this.results   = data.results
        this.total     = data.total
        this.expansion = data.expansion
        this.facets    = data.facets      // ← add
        this.query     = q
      } catch (e) {
        this.error = e.response?.data?.detail || 'Search failed'
      } finally {
        this.loading = false
      }
    },

    acceptCorrection() {
      if (this.spellResult?.corrected) {
        this.search(this.spellResult.corrected)
      }
      this.pendingCorrection = false
    },

    rejectCorrection() {
      this.search(this.spellResult.original)
      this.pendingCorrection = false
    },

    clearSpell() {
      this.spellResult       = null
      this.pendingCorrection = false
    },
  },
})