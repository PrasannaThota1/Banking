import { Component } from '@angular/core';
import { FormsModule, NgForm } from '@angular/forms';
import { RouterModule, Router } from '@angular/router';
import { AuthService } from '../services/auth.service';

@Component({
  standalone: true,
  selector: 'register-page',
  imports: [FormsModule, RouterModule],
  templateUrl: './register.page.html',
  styleUrl: './register.page.css'
})
export class RegisterPage {
  name = '';
  email = '';
  phone = '';
  password = '';
  constructor(private auth: AuthService, private router: Router) {}

  onSubmit(form?: NgForm) {
    if (form && form.invalid) return;
    this.auth.register({ name: this.name, email: this.email, phone: this.phone, password: this.password }).subscribe({
      next: () => this.router.navigate(['/login']),
      error: (err) => alert(err?.error?.message || 'Registration failed')
    });
  }
}
