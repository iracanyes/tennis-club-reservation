const AppRoutes =  {
  Login : "/login",
  AdminLogin : "/admin/login/",
  DashboardHome : "/home",
  DashboardAdmin : "/admin",
  ProfileChangePassword : "/profile/change_password",
  ProfileUpdate: "/profile/update",
  Subscribe : "/subscribe",
  SubscribePaymentSuccess : "/subscribe/payment/success",
  SubscribePaymentCancel : "/subscribe/payment/cancel",
  MyReservations : "/reservations/me",
  MemberList: "/members/",

}

type AppRoutes =  (typeof AppRoutes)[keyof typeof AppRoutes]

export default AppRoutes;

