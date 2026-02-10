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
    },
    accounts: {
      create: '/accounts/create',
      myAccounts: '/accounts/my-accounts',
      getAccount: '/accounts',
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
