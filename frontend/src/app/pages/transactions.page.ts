import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { TransactionService } from '../services/transaction.service';

@Component({
  standalone: true,
  selector: 'transactions-page',
  imports: [CommonModule],
  templateUrl: './transactions.page.html',
  styleUrl: './transactions.page.css'
})
export class TransactionsPage implements OnInit {
  transactions: any[] | null = null;
  loading = true;
  error: string | null = null;

  constructor(private transactionService: TransactionService) {}

  ngOnInit() {
    this.loadTransactions();
  }

  loadTransactions() {
    this.loading = true;
    this.error = null;
    this.transactionService.getHistory(50).subscribe({
      next: (data: any) => {
        this.transactions = data || [];
        this.loading = false;
      },
      error: (err) => {
        this.error = 'Failed to load transactions';
        this.loading = false;
        console.error(err);
      }
    });
  }
}
