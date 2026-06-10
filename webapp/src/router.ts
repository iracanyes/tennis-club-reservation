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
        component: () => import("@pages/AdminHomeView.vue"),
        name: "admin_home",
        meta: {
          requiresAuth: true,
          requiresAdmin: true
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
        path: AppRoutes.SubscribePaymentSuccess,
        component: () => import("@pages/StripeCheckoutSessionSuccessView.vue"),
        name: "stripe_checkout_success",
        meta: {
          requiresAuth: false
        }
      },
      {
        path: AppRoutes.SubscribePaymentCancel,
        component: () => import("@pages/StripeCheckoutSessionCancelView.vue"),
        name: "stripe_checkout_cancel",
        meta: {
          requiresAuth: false
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
        path: AppRoutes.ProfileUpdate,
        component: () => import("@components/security/ProfileUpdateView.vue"),
        name: "profile_update",
        meta: {
          requiresAuth: true
        }
      },
      {
        path: AppRoutes.MemberList,
        component: () => import("@pages/MembersView.vue"),
        name : "member_list",
        meta: {
          requiresAuth: true
        }
      },
      {
        path : AppRoutes.MemberUpdate,
        component: () => import("@pages/MemberUpdateView.vue"),
        name : "member_update",
        meta: {
          requiresAuth: true,
          requiresAdmin: true
        }
      },
      {
        path: AppRoutes.MyReservations,
        component: () => import("@pages/MyReservationsView.vue"),
        name: "my_reservations",
        meta: {
          requiresAuth: true
        }
      },
      {
        path: "/events",
        component: () => import("@pages/EventsView.vue"),
        name: "events",
        meta: {
          requiresAuth: true,
          requiresAdmin: true
        }
      },
      {
        path: "/courts",
        component: () => import("@pages/CourtsView.vue"),
        name: "courts",
        meta: {
          requiresAuth: true,
          requiresAdmin: true
        }
      },
      {
        path: "/courts/reservations",
        component: () => import("@pages/CourtReservationsView.vue"),
        name: "courts_reservations",
        meta: {
          requiresAuth: true,
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
  if(to.meta?.requiresAuth && !isNil(token)) {
    console.log(`router.beforeEach - to.meta.requiresAuth : ${(to.meta.requiresAuth as boolean)}`);
    // Redirect to login allowed
    if(to.path.includes("login")) return true;

    if(token.token.length > 0){
      console.log(`router.beforeEach - !isNil(tokenString) && JSON.parse(tokenString).token.length > 0 : ${!isNil(tokenString) && JSON.parse(tokenString).token.length > 0}`);
      // If admin's route and user not admin, redirect to admin login page
      if(to.meta?.requiresAdmin && token.type !== "admin") return { name : "admin-login"};

      return ["member", "admin"].includes(token.type);

    }else{
      console.log(`router.beforeEach - !(!isNil(tokenString) && JSON.parse(tokenString).token.length > 0) : REDIRECT TO LOGIN`);

      if(to.name?.contains("login")) return true;

      if(to.meta?.requiresAdmin || from.meta?.requiresAdmin){
        return {name: 'admin-login'};
      }else {
        // all pages are restricted, redirect to member login
        return {name: 'login'};
      }

    }
  }

  return true;

});

export { router  };