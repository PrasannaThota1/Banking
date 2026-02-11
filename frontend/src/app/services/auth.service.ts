import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { tap, map } from 'rxjs/operators';
import { API_CONFIG } from '../core/api.config';

@Injectable({providedIn: 'root'})
export class AuthService {
  private apiUrl = API_CONFIG.baseUrl;

  constructor(private http: HttpClient) {}

  register(data: any) {
    return this.http.post(`${this.apiUrl}${API_CONFIG.endpoints.auth.register}`, data);
  }

  login(data: any) {
    return this.http.post(`${this.apiUrl}${API_CONFIG.endpoints.auth.login}`, data).pipe(
      tap((response: any) => {
        // Store user info and tokens in localStorage if provided
        if (response.user) {
          localStorage.setItem('user', JSON.stringify(response.user));
        }
        if (response.access_token) {
          localStorage.setItem('access_token', response.access_token);
        }
        if (response.refresh_token) {
          localStorage.setItem('refresh_token', response.refresh_token);
        }
      })
    );
  }

  logout() {
    return this.http.post(`${this.apiUrl}${API_CONFIG.endpoints.auth.logout}`, {}).pipe(
      tap(() => {
        localStorage.removeItem('user');
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
      })
    );
  }

  getProfile() {
    return this.http.get(`${this.apiUrl}${API_CONFIG.endpoints.users.profile}`);
  }

  updateProfile(data: any) {
    return this.http.put(`${this.apiUrl}${API_CONFIG.endpoints.users.updateProfile}`, data);
  }

  // Admin: set KYC status for a user
  setKycStatus(userId: number, status: string) {
    return this.http.post(`${this.apiUrl}/users/admin/users/${userId}/kyc`, { status });
  }

  // Admin: list users
  listUsers() {
    return this.http.get(`${this.apiUrl}${API_CONFIG.endpoints.users.list}`);
  }

  isLoggedIn() {
    return !!localStorage.getItem('user');
  }

  getCurrentUser() {
    const user = localStorage.getItem('user');
    return user ? JSON.parse(user) : null;
  }
}
