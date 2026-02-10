import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { Chart, registerables } from 'chart.js';
import { AccountService } from '../services/account.service';
import { TransactionService } from '../services/transaction.service';

Chart.register(...registerables);

@Component({
  standalone: true,
  selector: 'dashboard-page',
  imports: [CommonModule, RouterModule],
  templateUrl: './dashboard.page.html',
  styleUrl: './dashboard.page.css'
})
export class DashboardPage implements OnInit {
  chart: any;
  summary: any = null;
  loading = true;
  error: string | null = null;

  constructor(
    private accountService: AccountService,
    private transactionService: TransactionService
  ) {}

  ngOnInit() {
    this.loadDashboard();
  }

  loadDashboard() {
    this.accountService.getAccountsList().subscribe({
      next: (accounts: any) => {
        // Calculate dashboard summary from accounts
        const totalBalance = accounts.reduce((sum: number, acc: any) => sum + (acc.balance || 0), 0);
        
        this.summary = {
          total_balance: totalBalance,
          account_count: accounts.length,
          accounts: accounts
        };

        // Load transaction history to count recent transactions
        this.transactionService.getHistory(5).subscribe({
          next: (txns: any) => {
            this.summary.recent_transactions = Array.isArray(txns) ? txns.length : 0;
            this.loading = false;
            this.renderChart();
          },
          error: () => {
            this.loading = false;
            this.renderChart();
          }
        });
      },
      error: (err) => {
        this.error = 'Failed to load dashboard';
        this.loading = false;
        console.error(err);
      }
    });
  }

  renderChart() {
    setTimeout(() => {
      const ctx = (document.getElementById('overviewChart') as HTMLCanvasElement)?.getContext('2d');
      if (!ctx) return;
      this.chart = new Chart(ctx, {
        type: 'line',
        data: {
          labels: ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],
          datasets: [
            { label: 'This Year', data: [1200,1500,1800,1400,1700,2000,2200,2400,2300,2100,2500,2700], borderColor: '#4f46e5', backgroundColor: 'rgba(79,70,229,0.08)', tension:0.35 },
            { label: 'Last Year', data: [900,1100,1300,1200,1400,1600,1800,1700,1600,1500,1700,1900], borderColor: '#06b6d4', backgroundColor: 'rgba(6,182,212,0.06)', tension:0.35 }
          ]
        },
        options: {
          responsive: true,
          scales: {
            x: { grid: { display: false }, ticks: { color: '#9aa6bb' } },
            y: { grid: { color: 'rgba(255,255,255,0.03)' }, ticks: { color: '#9aa6bb' } }
          },
          plugins: { legend: { labels: { color: '#cbd5e1' } } }
        }
      });
    }, 100);
  }
}
