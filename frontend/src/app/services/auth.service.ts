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
        // Store user info in localStorage if provided
        if (response.user) {
          localStorage.setItem('user', JSON.stringify(response.user));
        }
      })
    );
  }

  logout() {
    return this.http.post(`${this.apiUrl}${API_CONFIG.endpoints.auth.logout}`, {}).pipe(
      tap(() => {
        localStorage.removeItem('user');
      })
    );
  }

  getProfile() {
    return this.http.get(`${this.apiUrl}${API_CONFIG.endpoints.users.profile}`);
  }

  updateProfile(data: any) {
    return this.http.put(`${this.apiUrl}${API_CONFIG.endpoints.users.updateProfile}`, data);
  }

  isLoggedIn() {
    return !!localStorage.getItem('user');
  }

  getCurrentUser() {
    const user = localStorage.getItem('user');
    return user ? JSON.parse(user) : null;
  }
}
