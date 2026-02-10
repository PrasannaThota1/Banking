import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, NgForm } from '@angular/forms';
import { AccountService } from '../services/account.service';
import { Router } from '@angular/router';

@Component({
  standalone: true,
  selector: 'accounts-page',
  imports: [CommonModule, FormsModule],
  templateUrl: './accounts.page.html',
  styleUrl: './accounts.page.css'
})
export class AccountsPage implements OnInit {
  accounts: any[] = [];
  selectedAccount: any = null;
  activeMenu: number | null = null;
  loading = true;
  error: string | null = null;
  showCreateForm = false;
  creating = false;
  createError: string | null = null;

  // UI state for edit/delete/search
  showEditForm = false;
  editing = false;
  editError: string | null = null;
  editAccountData: any = null;
  searchTerm: string = '';

  accountTypes = ['CHECKING', 'SAVINGS', 'CREDIT'];
  newAccount = { account_type: 'CHECKING' };

  constructor(private accountService: AccountService, private router: Router) {}

  ngOnInit() {
    this.loadAccounts();
  }

  loadAccounts() {
    this.loading = true;
    this.error = null;
    this.accountService.listAccounts().subscribe({
      next: (data: any) => {
        this.accounts = data || [];
        this.loading = false;
      },
      error: (err: any) => {
        console.error('Error loading accounts:', err);
        this.error = err?.error?.detail || 'Failed to load accounts. Please try again.';
        this.loading = false;
      }
    });
  }

  openCreateForm() {
    this.showCreateForm = true;
    this.createError = null;
  }

  closeCreateForm() {
    this.showCreateForm = false;
    this.createError = null;
    this.newAccount = { account_type: 'CHECKING' };
  }

  onCreateAccount(form: NgForm) {
    if (form.invalid) return;

    this.creating = true;
    this.createError = null;

    this.accountService.createAccount({ account_type: this.newAccount.account_type }).subscribe({
      next: () => {
        this.creating = false;
        this.closeCreateForm();
        this.loadAccounts();
      },
      error: (err: any) => {
        this.creating = false;
        this.createError = err?.error?.detail || 'Failed to create account. Please try again.';
        console.error('Create account error:', err);
      }
    });
  }

  selectAccount(account: any) {
    this.selectedAccount = account;
  }

  viewAccountDetails(account: any, event: Event) {
    event.stopPropagation();
    this.activeMenu = null;
    this.selectedAccount = account;
  }

  toggleMenu(event: Event, account: any) {
    event.stopPropagation();
    this.activeMenu = this.activeMenu === account.id ? null : account.id;
  }

  editAccount(account: any) {
    console.log('Edit account:', account);
    this.activeMenu = null;
    this.editError = null;
    this.editAccountData = { ...account };
    this.showEditForm = true;
  }
  deleteAccount(account: any, event: Event) {
    event.stopPropagation();
    if (confirm(`Are you sure you want to delete account ${account.account_number}?`)) {
      this.activeMenu = null;
      this.accountService.deleteAccount(account.id).subscribe({
        next: () => {
          this.loadAccounts();
        },
        error: (err: any) => {
          console.error('Delete account error:', err);
          alert(err?.error?.detail || 'Failed to delete account.');
        }
      });
    }
  }

  saveEditAccount(form: NgForm) {
    if (!this.editAccountData) return;
    if (form.invalid) return;
    this.editing = true;
    this.editError = null;
    this.accountService.updateAccount(this.editAccountData.id, { account_type: this.editAccountData.account_type }).subscribe({
      next: (res: any) => {
        this.editing = false;
        this.showEditForm = false;
        this.editAccountData = null;
        this.loadAccounts();
      },
      error: (err: any) => {
        this.editing = false;
        this.editError = err?.error?.detail || 'Failed to update account.';
        console.error('Update account error:', err);
      }
    });
  }

  viewTransactions(account: any, event: Event) {
    event.stopPropagation();
    // Navigate to transactions page with account id as query param
    this.router.navigate(['/transactions'], { queryParams: { accountId: account.id } });
  }

  filteredAccounts() {
    if (!this.searchTerm) return this.accounts;
    const q = this.searchTerm.toLowerCase();
    return this.accounts.filter(a => (a.account_number || '').toLowerCase().includes(q) || (a.account_type || '').toLowerCase().includes(q));
  }

  getAccountIcon(accountType: string): string {
    const icons: { [key: string]: string } = {
      CHECKING: '🏦',
      SAVINGS: '💰',
      CREDIT: '💳'
    };
    return icons[accountType] || '💳';
  }

  maskAccountNumber(accountNumber: string): string {
    if (!accountNumber || accountNumber.length < 4) return accountNumber;
    const last4 = accountNumber.slice(-4);
    return `••••••••${last4}`;
  }
}
