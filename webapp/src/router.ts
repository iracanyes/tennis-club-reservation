import { createWebHistory, createRouter } from "vue-router";

// Chargement des vues
//import { LoginView, AdminLoginView } from "./components/security";
import { DashboardLayout } from "@layouts";
import { HomeView, NotFound } from "@pages";
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
        path: "/profile/change_password",
        component: () => import("@components/security/ChangePasswordView.vue"),
        name: "change_password",
        meta: {
          requiresAuth: true
        }
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
//@ts-ignore
router.beforeEach((to, from) => {
  const tokenString = localStorage.getItem(import.meta.env.VITE_TOKEN_KEY);

  // all routes are private except authentication routes
  if(to.meta.requiresAuth) {
    if(!isNil(tokenString) && JSON.parse(tokenString).token.length > 0){
      return true;
    }else{
      return {name: 'login'};
    }
  } else if (!to.path.includes("login")) {
    return {name: 'login'};
  }


});

export { router  };