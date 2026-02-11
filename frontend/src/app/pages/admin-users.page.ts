import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { AuthService } from '../services/auth.service';

@Component({
  standalone: true,
  selector: 'admin-users-page',
  imports: [CommonModule, RouterModule],
  templateUrl: './admin-users.page.html',
  styleUrl: './admin-users.page.css'
})
export class AdminUsersPage implements OnInit {
  users: any[] = [];
  loading = true;
  error: string | null = null;

  constructor(private authService: AuthService) {}

  ngOnInit() {
    this.loadUsers();
  }

  loadUsers() {
    this.loading = true;
    this.authService.listUsers().subscribe({
      next: (data: any) => { this.users = data || []; this.loading = false; },
      error: (err: any) => { this.error = 'Failed to load users'; this.loading = false; console.error(err); }
    });
  }

  setKyc(userId: number, status: string) {
    if (!confirm(`Set KYC status to ${status} for user ${userId}?`)) return;
    this.authService.setKycStatus(userId, status).subscribe({
      next: () => { alert('KYC updated'); this.loadUsers(); },
      error: (e) => { console.error(e); alert('Failed to update KYC'); }
    });
  }
}
