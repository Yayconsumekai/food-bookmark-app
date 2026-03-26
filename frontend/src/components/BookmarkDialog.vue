<template>
    <Teleport to="body">
      <div v-if="open" class="dialog-backdrop" @click.self="$emit('close')">
        <div class="dialog">
  
          <div class="dialog-header">
            <h3>Save Recipe</h3>
            <button class="btn-close" @click="$emit('close')">✕</button>
          </div>
  
          <div class="dialog-body">
            <p class="recipe-name">{{ recipeName }}</p>
  
            <!-- Star rating -->
            <label class="field-label">Your Rating</label>
            <StarRating v-model="rating" />
            <p v-if="ratingError" class="field-error">Please select a rating</p>
  
            <!-- Folder picker -->
            <label class="field-label">Save to Folder</label>
  
            <div v-if="folders.folders.length === 0" class="no-folders">
              No folders yet — create one below.
            </div>
  
            <div v-else class="folder-list">
              <button
                v-for="f in folders.folders"
                :key="f.id"
                class="folder-option"
                :class="{ selected: selectedFolderId === f.id }"
                @click="selectedFolderId = f.id"
              >
                📁 {{ f.name }}
                <span class="folder-count">({{ f.bookmark_count }})</span>
              </button>
            </div>
            <p v-if="folderError" class="field-error">Please select a folder</p>
  
            <!-- New folder inline -->
            <div class="new-folder-row">
              <input
                v-model="newFolderName"
                placeholder="New folder name..."
                @keyup.enter="createFolder"
              />
              <button @click="createFolder" :disabled="!newFolderName.trim()">
                + Create
              </button>
            </div>
          </div>
  
          <div class="dialog-footer">
            <button class="btn-cancel" @click="$emit('close')">Cancel</button>
            <button class="btn-save" @click="submit" :disabled="saving">
              {{ saving ? 'Saving...' : '🔖 Save' }}
            </button>
          </div>
  
        </div>
      </div>
    </Teleport>
  </template>
  
  <script setup>
  import { ref, watch } from 'vue'
  import StarRating         from './StarRating.vue'
  import { useFolderStore }   from '../stores/folder'
  import { useBookmarkStore } from '../stores/bookmark'
  
  const props = defineProps({
    open:       Boolean,
    recipeId:   Number,
    recipeName: String,
  })
  const emit = defineEmits(['close', 'saved'])
  
  const folders            = useFolderStore()
  const bookmarks          = useBookmarkStore()
  
  const rating             = ref(0)
  const selectedFolderId   = ref(null)
  const newFolderName      = ref('')
  const saving             = ref(false)
  const ratingError        = ref(false)
  const folderError        = ref(false)
  
  // Refresh folders whenever dialog opens
  watch(() => props.open, (val) => {
    if (val) {
      folders.fetchFolders()
      rating.value           = 0
      selectedFolderId.value = null
      ratingError.value      = false
      folderError.value      = false
    }
  })
  
  async function createFolder() {
    const name = newFolderName.value.trim()
    if (!name) return
    const folder = await folders.createFolder(name)
    selectedFolderId.value = folder.id
    newFolderName.value    = ''
  }
  
  async function submit() {
    ratingError.value = rating.value === 0
    folderError.value = !selectedFolderId.value
    if (ratingError.value || folderError.value) return
  
    saving.value = true
    try {
      await bookmarks.addBookmark(props.recipeId, selectedFolderId.value, rating.value)
      emit('saved')
      emit('close')
    } catch (e) {
      alert(e.response?.data?.detail || 'Failed to save bookmark')
    } finally {
      saving.value = false
    }
  }
  </script>
  
  <style scoped>
  .dialog-backdrop {
    position:        fixed; inset: 0;
    background:      rgba(0,0,0,0.45);
    display:         flex;
    align-items:     center;
    justify-content: center;
    z-index:         2000;
    padding:         1rem;
  }
  .dialog {
    background:    #fff;
    border-radius: 14px;
    width:         100%;
    max-width:     440px;
    box-shadow:    0 10px 40px rgba(0,0,0,0.2);
    overflow:      hidden;
  }
  .dialog-header {
    display:         flex;
    justify-content: space-between;
    align-items:     center;
    padding:         1rem 1.25rem;
    border-bottom:   1px solid #eee;
  }
  .dialog-header h3 { margin: 0; font-size: 1.1rem; }
  .btn-close {
    background: none; border: none;
    font-size: 1rem; cursor: pointer; color: #888;
  }
  .dialog-body      { padding: 1.25rem; display: flex; flex-direction: column; gap: 0.75rem; }
  .recipe-name      { font-weight: 600; font-size: 1rem; color: #333; margin: 0; }
  .field-label      { font-size: 0.85rem; font-weight: 600; color: #555; margin-bottom: -0.25rem; }
  .field-error      { font-size: 0.8rem; color: #e53e3e; margin: -0.5rem 0 0; }
  
  .folder-list      { display: flex; flex-direction: column; gap: 0.4rem; max-height: 180px; overflow-y: auto; }
  .folder-option {
    text-align:    left;
    background:    #f9f9f9;
    border:        2px solid transparent;
    border-radius: 8px;
    padding:       0.5rem 0.75rem;
    cursor:        pointer;
    font-size:     0.9rem;
    transition:    border-color 0.15s;
  }
  .folder-option.selected { border-color: #f6c90e; background: #fffbea; }
  .folder-count           { color: #999; font-size: 0.8rem; }
  .no-folders             { color: #aaa; font-size: 0.85rem; }
  
  .new-folder-row { display: flex; gap: 0.5rem; }
  .new-folder-row input {
    flex: 1; padding: 0.5rem 0.75rem;
    border: 1px solid #ddd; border-radius: 8px; font-size: 0.9rem;
  }
  .new-folder-row button {
    background: #f0f0f0; border: none;
    border-radius: 8px; padding: 0.5rem 0.85rem;
    cursor: pointer; font-size: 0.85rem; white-space: nowrap;
  }
  .new-folder-row button:disabled { opacity: 0.5; cursor: default; }
  
  .dialog-footer {
    display:       flex;
    justify-content: flex-end;
    gap:           0.75rem;
    padding:       1rem 1.25rem;
    border-top:    1px solid #eee;
  }
  .btn-cancel {
    background: none; border: 1px solid #ddd;
    border-radius: 8px; padding: 0.5rem 1rem;
    cursor: pointer; color: #666;
  }
  .btn-save {
    background: #f6c90e; border: none;
    border-radius: 8px; padding: 0.5rem 1.25rem;
    font-weight: 600; cursor: pointer;
  }
  .btn-save:disabled { opacity: 0.6; cursor: default; }
  </style>