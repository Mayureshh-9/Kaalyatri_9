import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ApiService } from '../../services/api.service';

@Component({
  selector: 'app-contact',
  templateUrl: './contact.component.html',
  styleUrls: ['./contact.component.scss'],
})
export class ContactComponent {
  form: FormGroup;
  submitting = false;
  successMessage = '';
  errorMessage = '';
  fieldErrors: { [key: string]: string } = {};

  constructor(private fb: FormBuilder, private api: ApiService) {
    this.form = this.fb.group({
      name: ['', [Validators.required, Validators.minLength(2)]],
      email: ['', [Validators.required, Validators.email]],
      phone: [''],
      subject: [''],
      message: ['', [Validators.required, Validators.minLength(10)]],
    });
  }

  controlInvalid(name: string): boolean {
    const c = this.form.get(name);
    return !!c && c.invalid && (c.dirty || c.touched);
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
    this.api.submitContact(this.form.value).subscribe({
      next: (res) => {
        this.submitting = false;
        this.successMessage = res.message || 'Thanks! We will be in touch.';
        this.form.reset();
      },
      error: (err) => {
        this.submitting = false;
        const body = err?.error;
        if (body?.fields) {
          this.fieldErrors = body.fields;
          this.errorMessage = 'Please fix the highlighted fields.';
        } else {
          this.errorMessage = body?.error || 'Something went wrong. Try again shortly.';
        }
      },
    });
  }
}
