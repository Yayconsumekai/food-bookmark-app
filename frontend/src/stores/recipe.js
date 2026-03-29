import { defineStore } from 'pinia'
import api from '../api/index.js'

export const useRecipeStore = defineStore('recipe', {
  state: () => ({
    cache:          {},   // { [recipeId]: RecipeDetail }
    selectedRecipe: null,
    loading:        false,
    error:          null,
  }),

  actions: {
    async fetchRecipe(id) {
      // Return from cache if already fetched
      if (this.cache[id]) {
        this.selectedRecipe = this.cache[id]
        return
      }

      this.loading = true
      this.error   = null
      try {
        const { data } = await api.get(`/api/search/recipe/${id}`)
      
        // Parse string fields into arrays for the modal
        data.ingredients_list = data.ingredients
          ? data.ingredients.split('\n').map(s => s.trim()).filter(Boolean)
          : []
      
        data.instructions_list = data.instructions
          ? data.instructions.split('\n').map(s => s.trim()).filter(Boolean)
          : []
      
        this.cache[id]      = data
        this.selectedRecipe = data
      } catch (e) {
        this.error = e.response?.data?.detail || 'Failed to load recipe'
      } finally {
        this.loading = false
      }
    },

    closeRecipe() {
      this.selectedRecipe = null
    },
  },
})