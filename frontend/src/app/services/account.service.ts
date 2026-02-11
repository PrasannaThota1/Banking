import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { API_CONFIG } from '../core/api.config';

@Injectable({providedIn: 'root'})
export class AccountService {
  private apiUrl = API_CONFIG.baseUrl;

  constructor(private http: HttpClient) {}

  createAccount(payload: any) {
    return this.http.post(`${this.apiUrl}${API_CONFIG.endpoints.accounts.create}`, payload);
  }

  createAccountRequest(payload: any) {
    return this.http.post(`${this.apiUrl}${API_CONFIG.endpoints.accounts.create}`, payload);
  }

  listRequests() {
    return this.http.get(`${this.apiUrl}${API_CONFIG.endpoints.accounts.requests}`);
  }

  approveRequest(requestId: number) {
    return this.http.post(`${this.apiUrl}${API_CONFIG.endpoints.accounts.approveRequest}/${requestId}/approve`, {});
  }

  rejectRequest(requestId: number, reason: string) {
    return this.http.post(`${this.apiUrl}${API_CONFIG.endpoints.accounts.rejectRequest}/${requestId}/reject`, { reason });
  }

  adminCreateAccount(payload: any) {
    return this.http.post(`${this.apiUrl}${API_CONFIG.endpoints.accounts.adminCreate}`, payload);
  }

  listAccounts() {
    return this.http.get(`${this.apiUrl}${API_CONFIG.endpoints.accounts.myAccounts}`);
  }

  getAccount(accountId: number) {
    return this.http.get(`${this.apiUrl}${API_CONFIG.endpoints.accounts.getAccount}/${accountId}`);
  }

  getAccountsList() {
    return this.listAccounts();
  }

  updateAccount(accountId: number, payload: any) {
    return this.http.put(`${this.apiUrl}${API_CONFIG.endpoints.accounts.getAccount}/${accountId}`, payload);
  }

  deleteAccount(accountId: number) {
    return this.http.delete(`${this.apiUrl}${API_CONFIG.endpoints.accounts.getAccount}/${accountId}`);
  }
}
