import { defineStore } from 'pinia'
import api from '../api/index.js'

export const useBookmarkStore = defineStore('bookmark', {
  state: () => ({
    allBookmarks:    [],
    folderBookmarks: [],
    loading:         false,
    error:           null,
  }),

  actions: {
    async fetchAll() {
      this.loading = true
      try {
        const { data } = await api.get('/api/bookmarks/')
        this.allBookmarks = data
      } finally {
        this.loading = false
      }
    },

    async fetchByFolder(folderId) {
      this.loading = true
      try {
        const { data } = await api.get(`/api/bookmarks/folder/${folderId}`)
        this.folderBookmarks = data
      } finally {
        this.loading = false
      }
    },

    async addBookmark(recipeId, folderId, rating) {
      const { data } = await api.post('/api/bookmarks/', {
        recipe_id: recipeId,
        folder_id: folderId,
        rating,
      })
      this.allBookmarks.unshift(data)
      return data
    },

    async updateBookmark(bookmarkId, payload) {
      const { data } = await api.put(`/api/bookmarks/${bookmarkId}`, payload)
      const i = this.allBookmarks.findIndex(b => b.id === bookmarkId)
      if (i !== -1) this.allBookmarks[i] = data
      return data
    },

    async removeBookmark(bookmarkId) {
      await api.delete(`/api/bookmarks/${bookmarkId}`)
      this.allBookmarks    = this.allBookmarks.filter(b => b.id !== bookmarkId)
      this.folderBookmarks = this.folderBookmarks.filter(b => b.id !== bookmarkId)
    },

    isBookmarked(recipeId) {
      return this.allBookmarks.some(b => b.recipe_id === recipeId)
    },

    getBookmark(recipeId) {
      return this.allBookmarks.find(b => b.recipe_id === recipeId) || null
    },
  },
})