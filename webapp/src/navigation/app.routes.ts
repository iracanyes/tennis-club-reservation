const AppRoutes =  {
  Login : "/login",
  AdminLogin : "/admin/login/",
  DashboardHome : "/home",
  DashboardAdmin : "/admin",
  ProfileChangePassword : "/profile/change_password",
  ProfileUpdate: "/profile/update",
  MemberCreate: "/member/create",
  MemberUpdate : "/members/update/:id",
  Subscribe : "/subscribe",
  SubscribePaymentSuccess : "/subscribe/payment/success",
  SubscribePaymentCancel : "/subscribe/payment/cancel",
  MyReservations : "/reservations/me",
  MemberList: "/members",
  EventsList: "/events",

}

type AppRoutes =  (typeof AppRoutes)[keyof typeof AppRoutes]

export default AppRoutes;

