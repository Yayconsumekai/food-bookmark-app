import { defineStore } from 'pinia'
import api from '../api/index.js'

export const useSearchStore = defineStore('search', {
  state: () => ({
    query:       '',
    results:     [],
    total:       0,
    loading:     false,
    error:       null,
    // spell correction state
    spellResult: null,   // { has_corrections, original, corrected, corrections }
    pendingCorrection: false,
  }),

  actions: {
    async search(q, offset = 0) {
      this.loading = true
      this.error   = null
      try {
        const { data } = await api.get('/api/search/', {
          params: { q, limit: 20, offset }
        })
        this.results = data.results
        this.total   = data.total
        this.query   = q
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