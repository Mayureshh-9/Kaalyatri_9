import { ComponentFixture, TestBed } from '@angular/core/testing';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { of } from 'rxjs';

import { ReviewsComponent } from './reviews.component';
import { ApiService } from '../../services/api.service';
import { Review } from '../../models/destination.model';

const mockReviews: Review[] = [
  { id: 1, destination_id: 1, rating: 5, comment: 'Amazing trip!', created_date: '2024-01-01' },
  { id: 2, destination_id: 1, rating: 4, comment: 'Loved it.',     created_date: '2024-01-02' }
];

describe('ReviewsComponent', () => {
  let component: ReviewsComponent;
  let fixture: ComponentFixture<ReviewsComponent>;
  let apiSpy: jasmine.SpyObj<ApiService>;

  beforeEach(async () => {
    apiSpy = jasmine.createSpyObj('ApiService', ['getReviews', 'createReview']);
    apiSpy.getReviews.and.returnValue(of(mockReviews));
    apiSpy.createReview.and.returnValue(of(mockReviews[0]));

    await TestBed.configureTestingModule({
      declarations: [ReviewsComponent],
      imports: [CommonModule, FormsModule, HttpClientTestingModule],
      providers: [{ provide: ApiService, useValue: apiSpy }]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ReviewsComponent);
    component = fixture.componentInstance;

    // Provide required @Input before detectChanges so ngOnInit can run cleanly
    component.destinationId = 1;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should load reviews on init', () => {
    expect(apiSpy.getReviews).toHaveBeenCalledWith(1);
    expect(component.reviews.length).toBe(2);
    expect(component.loading).toBeFalse();
  });

  it('should submit a review and append it to the list', () => {
    const newReview: Review = { id: 3, destination_id: 1, rating: 3, comment: 'Good.', created_date: '2024-01-03' };
    apiSpy.createReview.and.returnValue(of(newReview));

    component.newReview.rating = 3;
    component.newReview.comment = 'Good.';
    component.submitReview();

    expect(apiSpy.createReview).toHaveBeenCalled();
    expect(component.reviews).toContain(newReview);
    expect(component.newReview.comment).toBe('');
  });

  it('should not submit a review with an invalid rating', () => {
    component.newReview.rating = 0;
    component.submitReview();
    expect(apiSpy.createReview).not.toHaveBeenCalled();
  });
});
