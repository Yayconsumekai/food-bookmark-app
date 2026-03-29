import { defineStore } from 'pinia'
import api from '../api/index.js'

export const useSearchStore = defineStore('search', {
  state: () => ({
    query:             '',
    results:           [],
    total:             0,
    facets:            null,    
    loading:           false,
    error:             null,
    expansion:         null,
    currentPage:       1,   
    pageSize:          20,  
    spellResult:       null,
    pendingCorrection: false,
  }),

  getters: {
    totalPages: (state) => Math.ceil(state.total / state.pageSize),
  },

  actions: {
    async search(q, offset = 0) {
      this.loading   = true
      this.error     = null
      this.expansion = null
      try {
        const { data } = await api.get('/api/search/', {
          params: { q, limit: this.pageSize, offset }
        })
        this.results     = data.results
        this.total       = data.total
        this.expansion   = data.expansion
        this.facets      = data.facets
        this.query       = q
        this.currentPage = Math.floor(offset / this.pageSize) + 1  // ← add
      } catch (e) {
        this.error = e.response?.data?.detail || 'Search failed'
      } finally {
        this.loading = false
      }
    },
  
    async goToPage(page) {
      const offset = (page - 1) * this.pageSize
      await this.search(this.query, offset)
      window.scrollTo({ top: 0, behavior: 'smooth' })
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