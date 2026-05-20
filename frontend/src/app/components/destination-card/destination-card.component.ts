import { Component, Input } from '@angular/core';
import { Destination } from '../../models/destination.model';

@Component({
  selector: 'app-destination-card',
  templateUrl: './destination-card.component.html',
  styleUrls: ['./destination-card.component.scss'],
})
export class DestinationCardComponent {
  @Input({ required: true }) destination!: Destination;

  formatPrice(p: number): string {
    return '₹' + p.toLocaleString('en-IN');
  }
}
