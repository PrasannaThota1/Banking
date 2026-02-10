import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { API_CONFIG } from '../core/api.config';

@Injectable({providedIn: 'root'})
export class TransactionService {
  private apiUrl = API_CONFIG.baseUrl;

  constructor(private http: HttpClient) {}

  deposit(payload: any) {
    return this.http.post(`${this.apiUrl}${API_CONFIG.endpoints.transactions.deposit}`, payload);
  }

  withdraw(payload: any) {
    return this.http.post(`${this.apiUrl}${API_CONFIG.endpoints.transactions.withdraw}`, payload);
  }

  transfer(payload: any) {
    return this.http.post(`${this.apiUrl}${API_CONFIG.endpoints.transactions.transfer}`, payload);
  }

  getHistory(limit: number = 50) {
    const params = new HttpParams().set('limit', limit.toString());
    return this.http.get(`${this.apiUrl}${API_CONFIG.endpoints.transactions.history}`, { params });
  }
}
