<template>
    <nav class="navbar">
      <router-link to="/" class="nav-logo">🍴 FoodMark</router-link>
  
      <div class="nav-links">
        <router-link to="/"          class="nav-link">Home</router-link>
        <router-link to="/search"    class="nav-link">Search</router-link>
        <router-link to="/bookmarks" class="nav-link">Bookmarks</router-link>
      </div>
  
      <div class="nav-user">
        <span class="username">{{ auth.user?.username }}</span>
        <button class="btn-logout" @click="logout">Logout</button>
      </div>
    </nav>
  </template>
  
  <script setup>
  import { useAuthStore } from '../stores/auth'
  import { useRouter }    from 'vue-router'
  
  const auth   = useAuthStore()
  const router = useRouter()
  
  function logout() {
    auth.logout()
    router.push('/login')
  }
  </script>
  
  <style scoped>
  .navbar {
    display:          flex;
    align-items:      center;
    justify-content:  space-between;
    padding:          0.85rem 2rem;
    background:       #fff;
    border-bottom:    1px solid #eee;
    position:         sticky;
    top:              0;
    z-index:          500;
  }
  .nav-logo    {
    font-size: 1.15rem; font-weight: 800;
    text-decoration: none; color: #3d2c00;
  }
  .nav-links   { display: flex; gap: 1.5rem; }
  .nav-link    {
    text-decoration: none; color: #555;
    font-size: 0.9rem; font-weight: 500;
    transition: color 0.15s;
  }
  .nav-link:hover,
  .nav-link.router-link-active { color: #d97706; }
  
  .nav-user    { display: flex; align-items: center; gap: 0.85rem; }
  .username    { font-size: 0.85rem; color: #888; }
  .btn-logout  {
    background:    none;
    border:        1px solid #ddd;
    border-radius: 8px;
    padding:       0.3rem 0.75rem;
    font-size:     0.82rem;
    cursor:        pointer;
    color:         #666;
  }
  .btn-logout:hover { background: #fee2e2; color: #ef4444; border-color: #fca5a5; }
  </style>