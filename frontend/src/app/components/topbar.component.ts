import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, Router } from '@angular/router';
import { AuthService } from '../services/auth.service';

@Component({
  selector: 'app-topbar',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './topbar.component.html',
  styleUrl: './topbar.component.css'
})
export class TopbarComponent implements OnInit {
  isLoggedIn = false;
  currentUser: any = null;
  userInitials = '';

  constructor(private authService: AuthService, private router: Router) {}

  ngOnInit() {
    this.loadUserInfo();
  }

  loadUserInfo() {
    this.isLoggedIn = this.authService.isLoggedIn();
    if (this.isLoggedIn) {
      this.currentUser = this.authService.getCurrentUser();
      this.userInitials = this.getInitials(this.currentUser?.name || 'User');
    }
  }

  getInitials(name: string): string {
    return name
      .split(' ')
      .map(n => n[0])
      .join('')
      .toUpperCase()
      .slice(0, 2);
  }

  onLogout() {
    if (confirm('Are you sure you want to logout?')) {
      this.authService.logout().subscribe({
        next: () => {
          this.isLoggedIn = false;
          this.currentUser = null;
          this.router.navigate(['/login']);
        },
        error: (err) => {
          console.error('Logout error:', err);
          // Still logout locally even if API call fails
          localStorage.removeItem('user');
          this.router.navigate(['/login']);
        }
      });
    }
  }
}
