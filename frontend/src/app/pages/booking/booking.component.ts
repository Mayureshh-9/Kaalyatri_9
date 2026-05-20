import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute } from '@angular/router';
import { ApiService } from '../../services/api.service';
import { Destination } from '../../models/destination.model';

@Component({
  selector: 'app-booking',
  templateUrl: './booking.component.html',
  styleUrls: ['./booking.component.scss'],
})
export class BookingComponent implements OnInit {
  destinations: Destination[] = [];
  form: FormGroup;
  loading = true;
  submitting = false;
  successMessage = '';
  errorMessage = '';
  fieldErrors: { [key: string]: string } = {};
  minDate = '';

  constructor(
    private fb: FormBuilder,
    private api: ApiService,
    private route: ActivatedRoute,
  ) {
    const tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate() + 1);
    this.minDate = tomorrow.toISOString().split('T')[0];

    this.form = this.fb.group({
      destinationId: [null, [Validators.required]],
      fullName: ['', [Validators.required, Validators.minLength(2)]],
      email: ['', [Validators.required, Validators.email]],
      phone: ['', [Validators.required, Validators.pattern(/^[0-9+\-\s()]{7,20}$/)]],
      travelers: [1, [Validators.required, Validators.min(1), Validators.max(20)]],
      travelDate: ['', [Validators.required]],
      notes: [''],
    });
  }

  ngOnInit(): void {
    this.api.getDestinations().subscribe({
      next: (items) => {
        this.destinations = items;
        this.loading = false;
        const preId = Number(this.route.snapshot.paramMap.get('id'));
        if (preId && items.some((d) => d.id === preId)) {
          this.form.patchValue({ destinationId: preId });
        }
      },
      error: () => {
        this.loading = false;
        this.errorMessage = 'Cannot reach the booking grid. Please make sure the API is running.';
      },
    });
  }

  controlInvalid(name: string): boolean {
    const c = this.form.get(name);
    return !!c && c.invalid && (c.dirty || c.touched);
  }

  selectedDestination(): Destination | undefined {
    const id = Number(this.form.value.destinationId);
    return this.destinations.find((d) => d.id === id);
  }

  estimatedTotal(): number {
    const d = this.selectedDestination();
    const travelers = Number(this.form.value.travelers) || 0;
    return d ? d.priceInr * travelers : 0;
  }

  formatPrice(p: number): string {
    return '₹' + p.toLocaleString('en-IN');
  }

  submit(): void {
    this.successMessage = '';
    this.errorMessage = '';
    this.fieldErrors = {};

    if (this.form.invalid) {
      this.form.markAllAsTouched();
      return;
    }

    this.submitting = true;
    this.api.createBooking(this.form.value).subscribe({
      next: (res) => {
        this.submitting = false;
        this.successMessage = res.message || 'Booking confirmed.';
        this.form.reset({ travelers: 1, destinationId: null });
      },
      error: (err) => {
        this.submitting = false;
        const body = err?.error;
        if (body?.fields) {
          this.fieldErrors = body.fields;
          this.errorMessage = 'Please fix the highlighted fields.';
        } else {
          this.errorMessage = body?.error || 'Booking failed. Please try again.';
        }
      },
    });
  }
}
