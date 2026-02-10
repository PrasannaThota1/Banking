import { Component } from '@angular/core';
import { FormsModule, NgForm } from '@angular/forms';
import { RouterModule, Router } from '@angular/router';
import { AuthService } from '../services/auth.service';

@Component({
  standalone: true,
  selector: 'login-page',
  imports: [FormsModule, RouterModule],
  templateUrl: './login.page.html',
  styleUrl: './login.page.css'
})
export class LoginPage {
  email = '';
  password = '';
  remember = false;
  constructor(private auth: AuthService, private router: Router) {}

  onSubmit(form?: NgForm) {
    if (form && form.invalid) return;
    this.auth.login({ email: this.email, password: this.password }).subscribe({
      next: () => this.router.navigate(['/dashboard']),
      error: (err) => alert(err?.error?.message || 'Login failed')
    });
  }
}
