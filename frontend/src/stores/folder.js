import { defineStore } from 'pinia'
import api from '../api/index.js'

export const useFolderStore = defineStore('folder', {
  state: () => ({
    folders: [],
    loading: false,
    error:   null,
  }),

  actions: {
    async fetchFolders() {
      this.loading = true
      try {
        const { data } = await api.get('/api/folders/')
        this.folders = data
      } catch (e) {
        this.error = e.response?.data?.detail || 'Failed to load folders'
      } finally {
        this.loading = false
      }
    },

    async createFolder(name) {
      const { data } = await api.post('/api/folders/', { name })
      this.folders.push(data)
      return data
    },

    async updateFolder(id, name) {
      const { data } = await api.put(`/api/folders/${id}`, { name })
      const i = this.folders.findIndex(f => f.id === id)
      if (i !== -1) this.folders[i] = data
    },

    async deleteFolder(id) {
      await api.delete(`/api/folders/${id}`)
      this.folders = this.folders.filter(f => f.id !== id)
    },
  },
})