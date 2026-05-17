import { createWebHistory, createRouter } from "vue-router";
import { DashboardLayout } from "@layouts";
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
        component: () => import("@pages/HomeView.vue"),
        name: "home",
        meta: {
          requiresAuth: true
        }
      },
      {
        path: "/admin",
        component: () => import("@pages/DashboardHome.vue"),
        name: "admin_home",
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
      {
        path: "/subscribe",
        component: () => import("@pages/SubscribeView.vue"),
        name: "subscribe",
        meta: {
          requiresAuth: true
        }
      },
      {
        path: "/subscribe/payment/success",
        component: () => import("@pages/StripeCheckoutSessionSuccessView.vue"),
        name: "stripe_checkout_success",
        meta: {
          requiresAuth: false
        }
      },
      {
        path: "/subscribe/payment/cancel",
        component: () => import("@pages/StripeCheckoutSessionSuccessView.vue"),
        name: "stripe_checkout_cancel",
        meta: {
          requiresAuth: false
        }
      }
    ]
  },
  {
    path: "/:pathMatch(.*)*",
    component: () => import("@pages/NotFound.vue"),
    name: "not-found"
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

// Global security route guards
//@ts-ignore
router.beforeEach((to, from) => {
  const tokenString = localStorage.getItem(import.meta.env.VITE_TOKEN_KEY);

  console.log(`router.beforeEach - to.path : ${to.path}`);
  if(to.path.startsWith("http")){
    console.log(`router.beforeEach - to.path.startsWith("http") && to.meta.requiresAuth : ${to.path.startsWith("http") && to.meta.requiresAuth}`);
    return true;
  }

  // all routes are private except authentication routes
  if(to.meta?.requiresAuth) {
    console.log(`router.beforeEach - to.meta.requiresAuth : ${(to.meta.requiresAuth as boolean)}`);

    if(to.path.includes("login")) return true;

    if(!isNil(tokenString) && JSON.parse(tokenString).token.length > 0){
      console.log(`router.beforeEach - !isNil(tokenString) && JSON.parse(tokenString).token.length > 0 : ${!isNil(tokenString) && JSON.parse(tokenString).token.length > 0}`);
      return true;
    }else{
      console.log(`router.beforeEach - !(!isNil(tokenString) && JSON.parse(tokenString).token.length > 0) : REDIRECT TO LOGIN`);
      return {name: 'login'};
    }
  }

  return true;

});

export { router  };