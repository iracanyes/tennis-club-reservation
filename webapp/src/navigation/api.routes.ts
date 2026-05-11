const ApiRoutes = {
  Home : '/dashboard',
  MemberLogin : '/auth/member/login',
  AdminLogin : '/auth/admin/login',
  AdminLoginGoogle: '/auth/admin/login/google',
  UpdatePassword : '/auth/change_password',
  RefreshToken : '/auth/refresh_token',
  Me : 'auth/token/verify',
  Logout : '/logout',
  CsrfToken : '/auth/csrf_token',
  ChangePassword : '/auth/change_password',
  MemberList : '/api/members',
} as const

export default ApiRoutes

