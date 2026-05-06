import { createWebHistory, createRouter } from "vue-router";

// Chargement des vues
import { LoginView, AdminLoginView } from "./components/security";
import {DashboardLayout} from "@layouts";
import {DashboardHome, HomeView, NotFound } from "@pages";
import {isNil} from "lodash";

// Define routes
const routes = [
  // Redirection
  //{ path: '/', redirect: '/sign-in' },
  { path: "/sign-in", redirect: "/login" },
  { path: "/admin/sign-in", redirect: "/admin/login/" },
  { path: "/admin/login", redirect: "/admin/login/" },
  {
    path: "/login",
    component : () => import("@components/security/LoginView.vue"),
    name: "login"
  },
  {
    path: "/admin/login/",
    component: () => import("@components/security/AdminLoginView.vue"),
    name: "admin-login"
  },
  {
    path : "/dashboard",
    component: DashboardLayout,
    children: [
      {
        path: "/home",
        component: HomeView,
        name: "home",
        meta: {
          requiresAuth: true
        }
      },
      {
        path: "home",
        component: DashboardHome,
        name: "dashboard"
      },
    ]
  },
  { path: "/:pathMatch(.*)*", component: NotFound, name: "not-found" },
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

// Global security route guards
router.beforeEach((to, from) => {
  const tokenString = localStorage.getItem(import.meta.env.VITE_TOKEN_KEY);

  console.log(`Route guard - tokenString: ${tokenString!}`);

  if(!isNil(tokenString) && JSON.parse(tokenString).token.length > 0) {
    return true
  }else if (!to.path.includes("login")) {
    return {name: 'login'};
  }


});

export { router  };