import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import LoginView    from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import HomeView     from '../views/HomeView.vue'  // we'll build this in Step 7
import SearchView from '../views/SearchView.vue'

const routes = [
  { path: '/login',    component: LoginView },
  { path: '/register', component: RegisterView },
  {
    path: '/',
    component: HomeView,
    meta: { requiresAuth: true },   // ← protected route
  },
  {
    path: '/search',
    component: SearchView,
    meta: { requiresAuth: true },
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// Auth guard — redirect to /login if not authenticated
router.beforeEach((to) => {
  const auth = useAuthStore()
  if (to.meta.requiresAuth && !auth.isLoggedIn) {
    return '/login'
  }
})

export default router