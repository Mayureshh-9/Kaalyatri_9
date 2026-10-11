import { Component, Input, OnInit } from '@angular/core';
import { ApiService } from '../../services/api.service';
import { TourItinerary } from '../../models/destination.model';

@Component({
  selector: 'app-itineraries',
  templateUrl: './itineraries.component.html',
  styleUrls: ['./itineraries.component.scss']
})
export class ItinerariesComponent implements OnInit {
  @Input() destinationId!: number;
  itineraries: TourItinerary[] = [];
  loading = true;

  constructor(private api: ApiService) {}

  ngOnInit(): void {
    if (this.destinationId) {
      this.api.getItineraries(this.destinationId).subscribe({
        next: (data: TourItinerary[]) => {
          this.itineraries = data;
          this.loading = false;
        },
        error: () => this.loading = false
      });
    }
  }
}
