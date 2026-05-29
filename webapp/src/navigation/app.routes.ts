const AppRoutes =  {
  Login : "/login",
  AdminLogin : "/admin/login/",
  DashboardHome : "/home",
  DashboardAdmin : "/admin",
  ProfileChangePassword : "/profile/change_password",
  Subscribe : "/subscribe",
  MyReservations : "/reservations/me",
}

type AppRoutes =  (typeof AppRoutes)[keyof typeof AppRoutes]

export default AppRoutes;

