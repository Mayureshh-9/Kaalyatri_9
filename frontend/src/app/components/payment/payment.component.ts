import { Component, Input, Output, EventEmitter } from '@angular/core';
import { ApiService } from '../../services/api.service';
import { PaymentPayload } from '../../models/destination.model';

@Component({
  selector: 'app-payment',
  templateUrl: './payment.component.html',
  styleUrls: ['./payment.component.scss']
})
export class PaymentComponent {
  @Input() bookingId!: number;
  @Input() amount!: number;
  @Output() paymentSuccess = new EventEmitter<boolean>();
  
  processing = false;
  success = false;
  error = '';

  constructor(private api: ApiService) {}

  processPayment(): void {
    if (!this.bookingId || !this.amount) return;
    
    this.processing = true;
    this.error = '';

    const payload: PaymentPayload = {
      booking_id: this.bookingId,
      amount: this.amount,
      status: 'Completed',
      transaction_id: 'TXN-' + Math.floor(Math.random() * 1000000000)
    };

    // Simulate network delay for payment processing
    setTimeout(() => {
      this.api.createPayment(payload).subscribe({
        next: () => {
          this.processing = false;
          this.success = true;
          this.paymentSuccess.emit(true);
        },
        error: () => {
          this.processing = false;
          this.error = 'Payment failed. Please try again.';
        }
      });
    }, 1500);
  }
}
