import { Routes } from '@angular/router';
import { HomePage } from './pages/home.page';
import { AccountsPage } from './pages/accounts.page';
import { TransactionsPage } from './pages/transactions.page';
import { DashboardPage } from './pages/dashboard.page';
import { LoginPage } from './pages/login.page';
import { RegisterPage } from './pages/register.page';
import { AuthGuard } from './core/auth.guard';

export const routes: Routes = [
  { path: '', component: HomePage },
  { path: 'login', component: LoginPage },
  { path: 'register', component: RegisterPage },
  { path: 'dashboard', component: DashboardPage, canActivate: [AuthGuard] },
  { path: 'accounts', component: AccountsPage, canActivate: [AuthGuard] },
  { path: 'transactions', component: TransactionsPage, canActivate: [AuthGuard] }
];
