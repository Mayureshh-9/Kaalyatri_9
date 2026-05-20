import { Component, OnInit } from '@angular/core';
import { ApiService } from '../../services/api.service';
import { Destination } from '../../models/destination.model';

@Component({
  selector: 'app-destinations',
  templateUrl: './destinations.component.html',
  styleUrls: ['./destinations.component.scss'],
})
export class DestinationsComponent implements OnInit {
  all: Destination[] = [];
  filtered: Destination[] = [];
  loading = true;
  apiOffline = false;
  query = '';
  difficulty = 'all';

  constructor(private api: ApiService) {}

  ngOnInit(): void {
    this.api.getDestinations().subscribe({
      next: (items) => {
        this.all = items;
        this.filtered = items;
        this.loading = false;
      },
      error: () => {
        this.loading = false;
        this.apiOffline = true;
      },
    });
  }

  applyFilters(): void {
    const q = this.query.trim().toLowerCase();
    this.filtered = this.all.filter((d) => {
      const matchesQuery =
        !q ||
        d.name.toLowerCase().includes(q) ||
        d.era.toLowerCase().includes(q) ||
        d.yearLabel.toLowerCase().includes(q);
      const matchesDiff = this.difficulty === 'all' || d.difficulty === this.difficulty;
      return matchesQuery && matchesDiff;
    });
  }
}
