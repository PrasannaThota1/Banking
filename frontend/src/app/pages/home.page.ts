import { Component } from '@angular/core';
import { RouterModule } from '@angular/router';

@Component({
  standalone: true,
  selector: 'home-page',
  imports: [RouterModule],
  templateUrl: './home.page.html',
  styleUrl: './home.page.css'
})
export class HomePage {}
