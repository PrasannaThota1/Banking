import { Component } from '@angular/core';
import { Router, RouterOutlet, NavigationEnd } from '@angular/router';
import { CommonModule } from '@angular/common';
import { SidebarComponent } from './components/sidebar.component';
import { TopbarComponent } from './components/topbar.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, RouterOutlet, SidebarComponent, TopbarComponent],
  template: `
  <div class="app-shell">
    <ng-container *ngIf="showShell">
      <app-sidebar></app-sidebar>
    </ng-container>

    <div class="main">
      <ng-container *ngIf="showShell">
        <app-topbar></app-topbar>
      </ng-container>

      <router-outlet></router-outlet>
    </div>
  </div>
  `
})
export class AppComponent {
  showShell = true;
  private hideOn = ['/', '/login', '/register'];

  constructor(private router: Router) {
    this.updateShellVisibility(this.router.url);
    this.router.events.subscribe((ev) => {
      if (ev instanceof NavigationEnd) this.updateShellVisibility(ev.urlAfterRedirects);
    });
  }

  private updateShellVisibility(url: string) {
    this.showShell = !this.hideOn.includes(url.split('?')[0]);
  }
}
