<template>
    <div class="folder-manager">
      <div class="fm-header">
        <h3>My Folders</h3>
        <button class="btn-new" @click="showCreate = true">+ New Folder</button>
      </div>
  
      <!-- Create input -->
      <div v-if="showCreate" class="create-row">
        <input
          v-model="createName"
          placeholder="Folder name..."
          @keyup.enter="submitCreate"
          autofocus
        />
        <button @click="submitCreate" :disabled="!createName.trim()">Create</button>
        <button class="btn-cancel" @click="showCreate = false; createName = ''">Cancel</button>
      </div>
  
      <!-- Folder list -->
      <div v-if="folders.loading" class="fm-loading">Loading folders...</div>
  
      <ul v-else class="folder-list">
        <li
          v-for="folder in folders.folders"
          :key="folder.id"
          class="folder-item"
          :class="{ active: selectedId === folder.id }"
          @click="$emit('select', folder)"
        >
          <!-- Rename mode -->
          <template v-if="editingId === folder.id">
            <input
              v-model="editName"
              class="edit-input"
              @keyup.enter="submitRename(folder.id)"
              @keyup.escape="editingId = null"
            />
            <button class="btn-icon" @click="submitRename(folder.id)">✓</button>
            <button class="btn-icon" @click="editingId = null">✕</button>
          </template>
  
          <!-- Normal mode -->
          <template v-else>
            <span class="folder-icon">📁</span>
            <span class="folder-name">{{ folder.name }}</span>
            <span class="folder-count">{{ folder.bookmark_count }}</span>
            <div class="folder-actions">
              <button class="btn-icon" title="Rename"
                @click.stop="startEdit(folder)">✏️</button>
              <button class="btn-icon danger" title="Delete"
                @click.stop="confirmDelete(folder)">🗑</button>
            </div>
          </template>
        </li>
  
        <li v-if="folders.folders.length === 0" class="empty-folders">
          No folders yet. Create one above.
        </li>
      </ul>
  
      <!-- Delete confirmation -->
      <div v-if="pendingDelete" class="delete-confirm">
        <p>Delete <strong>{{ pendingDelete.name }}</strong>? All bookmarks inside will be removed.</p>
        <div class="confirm-actions">
          <button class="btn-danger" @click="submitDelete">Yes, delete</button>
          <button @click="pendingDelete = null">Cancel</button>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import { useFolderStore } from '../stores/folder'
  
  defineProps({ selectedId: Number })
  defineEmits(['select'])
  
  const folders     = useFolderStore()
  const showCreate  = ref(false)
  const createName  = ref('')
  const editingId   = ref(null)
  const editName    = ref('')
  const pendingDelete = ref(null)
  
  onMounted(() => folders.fetchFolders())
  
  async function submitCreate() {
    if (!createName.value.trim()) return
    await folders.createFolder(createName.value.trim())
    createName.value = ''
    showCreate.value = false
  }
  
  function startEdit(folder) {
    editingId.value = folder.id
    editName.value  = folder.name
  }
  
  async function submitRename(id) {
    if (!editName.value.trim()) return
    await folders.updateFolder(id, editName.value.trim())
    editingId.value = null
  }
  
  function confirmDelete(folder) {
    pendingDelete.value = folder
  }
  
  async function submitDelete() {
    await folders.deleteFolder(pendingDelete.value.id)
    pendingDelete.value = null
  }
  </script>
  
  <style scoped>
  .folder-manager   { background: #fff; border-radius: 12px; padding: 1.25rem; border: 1px solid #eee; }
  .fm-header        { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; }
  .fm-header h3     { margin: 0; font-size: 1rem; }
  .btn-new          { background: #f6c90e; border: none; border-radius: 8px; padding: 0.4rem 0.85rem; cursor: pointer; font-size: 0.85rem; font-weight: 600; }
  
  .create-row       { display: flex; gap: 0.5rem; margin-bottom: 0.75rem; }
  .create-row input { flex: 1; padding: 0.45rem 0.75rem; border: 1px solid #ddd; border-radius: 8px; font-size: 0.9rem; }
  .create-row button { background: #f6c90e; border: none; border-radius: 8px; padding: 0.45rem 0.85rem; cursor: pointer; font-size: 0.85rem; }
  .btn-cancel       { background: none !important; border: 1px solid #ddd !important; color: #888; }
  
  .folder-list      { list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: 0.3rem; }
  .folder-item {
    display:       flex;
    align-items:   center;
    gap:           0.5rem;
    padding:       0.6rem 0.75rem;
    border-radius: 8px;
    cursor:        pointer;
    transition:    background 0.1s;
  }
  .folder-item:hover  { background: #f9f9f9; }
  .folder-item.active { background: #fffbea; }
  .folder-name        { flex: 1; font-size: 0.9rem; }
  .folder-count       { font-size: 0.78rem; color: #aaa; background: #f0f0f0; border-radius: 10px; padding: 0.1rem 0.45rem; }
  .folder-actions     { display: none; gap: 0.25rem; }
  .folder-item:hover .folder-actions { display: flex; }
  
  .btn-icon           { background: none; border: none; cursor: pointer; font-size: 0.9rem; padding: 0.1rem 0.3rem; border-radius: 4px; }
  .btn-icon:hover     { background: #eee; }
  .btn-icon.danger:hover { background: #fee2e2; }
  
  .edit-input         { flex: 1; padding: 0.3rem 0.5rem; border: 1px solid #f6c90e; border-radius: 6px; font-size: 0.9rem; }
  .empty-folders      { color: #aaa; font-size: 0.85rem; padding: 0.5rem 0; text-align: center; }
  .fm-loading         { color: #aaa; font-size: 0.85rem; padding: 0.5rem; }
  
  .delete-confirm {
    margin-top: 1rem; padding: 1rem;
    background: #fff5f5; border: 1px solid #fca5a5;
    border-radius: 8px; font-size: 0.9rem;
  }
  .confirm-actions    { display: flex; gap: 0.5rem; margin-top: 0.75rem; }
  .btn-danger         { background: #ef4444; color: #fff; border: none; border-radius: 8px; padding: 0.4rem 0.85rem; cursor: pointer; }
  </style>