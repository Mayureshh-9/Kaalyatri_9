import { Component, Input, OnInit } from '@angular/core';
import { ApiService } from '../../services/api.service';
import { Review, ReviewPayload } from '../../models/destination.model';

@Component({
  selector: 'app-reviews',
  templateUrl: './reviews.component.html',
  styleUrls: ['./reviews.component.scss']
})

export class ReviewsComponent implements OnInit {
  @Input() destinationId!: number;
  reviews: Review[] = [];
  loading = true;

  newReview: ReviewPayload = {
    destination_id: 0,
    rating: 5,
    comment: ''
  };

  constructor(private api: ApiService) {}

  ngOnInit(): void {
    if (this.destinationId) {
      this.newReview.destination_id = this.destinationId;
      this.loadReviews();
    }
  }

  loadReviews(): void {
    this.api.getReviews(this.destinationId).subscribe({
      next: (data: Review[]) => {
        this.reviews = data;
        this.loading = false;
      },
      error: () => this.loading = false
    });
  }

  submitReview(): void {
    if (this.newReview.rating >= 1 && this.newReview.rating <= 5) {
      this.api.createReview(this.newReview).subscribe({
        next: (review: Review) => {
          this.reviews.push(review);
          this.newReview.comment = '';
        }
      });
    }
  }
}
