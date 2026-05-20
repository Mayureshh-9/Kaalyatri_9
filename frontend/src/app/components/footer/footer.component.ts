import { Component } from '@angular/core';
import { ApiService } from '../../services/api.service';

@Component({
  selector: 'app-footer',
  templateUrl: './footer.component.html',
  styleUrls: ['./footer.component.scss'],
})
export class FooterComponent {
  email = '';
  status: 'idle' | 'loading' | 'ok' | 'error' = 'idle';
  feedback = '';
  year = new Date().getFullYear();

  constructor(private api: ApiService) {}

  subscribe(): void {
    if (!this.email) return;
    this.status = 'loading';
    this.api.subscribeNewsletter(this.email).subscribe({
      next: (res) => {
        this.status = 'ok';
        this.feedback = res.message || 'Subscribed!';
        this.email = '';
      },
      error: (err) => {
        this.status = 'error';
        this.feedback = err?.error?.error || 'Could not subscribe.';
      },
    });
  }
}
