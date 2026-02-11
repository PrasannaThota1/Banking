// API configuration for frontend
export const API_CONFIG = {
  baseUrl: 'http://localhost:8000',
  endpoints: {
    auth: {
      register: '/auth/register',
      login: '/auth/login',
      logout: '/auth/logout',
      refreshToken: '/auth/refresh-token',
    },
    users: {
      profile: '/users/profile',
      updateProfile: '/users/profile',
      list: '/users/admin/list',
    },
    accounts: {
      create: '/accounts/create',
      myAccounts: '/accounts/my-accounts',
      getAccount: '/accounts',
      requests: '/accounts/requests',
      approveRequest: '/accounts/requests',
      rejectRequest: '/accounts/requests',
      adminCreate: '/accounts/admin/create'
    },
    transactions: {
      deposit: '/transactions/deposit',
      withdraw: '/transactions/withdraw',
      transfer: '/transactions/transfer',
      history: '/transactions/history',
    },
    dashboard: {
      summary: '/dashboard/summary',
    }
  }
};
