import {createRouter, createWebHistory} from "vue-router";
import {DashboardLayout} from "@layouts";
import {isNil} from "lodash";
import AppRoutes from "@navigation/app.routes.ts";

// Define routes
const routes = [
  // Redirection
  //{ path: '/', redirect: '/sign-in' },
  { path: "/sign-in", redirect: "/login" },
  { path: "/admin/sign-in", redirect: "/admin/login/" },
  { path: "/admin/login", redirect: "/admin/login/" },
  {
    path: AppRoutes.Login,
    component : () => import("@components/security/LoginView.vue"),
    name: "login"
  },
  {
    path: AppRoutes.AdminLogin,
    component: () => import("@components/security/AdminLoginView.vue"),
    name: "admin-login"
  },
  {
    path : "/dashboard",
    component: DashboardLayout,
    children: [
      {
        path: AppRoutes.DashboardHome,
        component: () => import("@pages/HomeView.vue"),
        name: "home",
        meta: {
          requiresAuth: true
        }
      },
      {
        path: AppRoutes.DashboardAdmin,
        component: () => import("@pages/DashboardHome.vue"),
        name: "admin_home",
        meta: {
          requiresAuth: true,
          requiresAdmin: true
        }
      },
      {
        path: AppRoutes.ProfileChangePassword,
        component: () => import("@components/security/ChangePasswordView.vue"),
        name: "change_password",
        meta: {
          requiresAuth: true
        }
      },
      {
        path: AppRoutes.Subscribe,
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
        component: () => import("@pages/StripeCheckoutSessionCancelView.vue"),
        name: "stripe_checkout_cancel",
        meta: {
          requiresAuth: false
        }
      },
      {
        path: "/reservations/me",
        component: () => import("@pages/MyReservationsView.vue"),
        name: "my_reservations",
        meta: {
          requiresAuth: true
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
  const token = isNil(tokenString) ? null : JSON.parse(tokenString);

  console.log(`router.beforeEach - to.path : ${to.path}`);
  if(to.path.startsWith("http")){
    console.log(`router.beforeEach - to.path.startsWith("http") && to.meta.requiresAuth : ${to.path.startsWith("http") && to.meta.requiresAuth}`);
    return true;
  }

  // all routes are private except authentication routes
  if(to.meta?.requiresAuth) {
    console.log(`router.beforeEach - to.meta.requiresAuth : ${(to.meta.requiresAuth as boolean)}`);
    // Redirect to login allowed
    if(to.path.includes("login")) return true;

    if(!isNil(token) && token.token.length > 0){
      console.log(`router.beforeEach - !isNil(tokenString) && JSON.parse(tokenString).token.length > 0 : ${!isNil(tokenString) && JSON.parse(tokenString).token.length > 0}`);
      if(to.meta?.requiresAdmin && token.type === "admin") return true;

      return ["member", "admin"].includes(token.type);

    }else{
      console.log(`router.beforeEach - !(!isNil(tokenString) && JSON.parse(tokenString).token.length > 0) : REDIRECT TO LOGIN`);
      if(to.meta?.requiresAdmin){
        return {name: 'admin-login'};
      }else {
        return {name: 'login'};
      }

    }
  }

  return true;

});

export { router  };