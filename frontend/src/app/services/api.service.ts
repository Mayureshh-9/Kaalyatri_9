import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';
import {
  ApiResponse,
  BookingPayload,
  ContactPayload,
  Destination,
} from '../models/destination.model';

@Injectable({ providedIn: 'root' })
export class ApiService {
  private readonly base = environment.apiBaseUrl;

  constructor(private http: HttpClient) {}

  getDestinations(featuredOnly = false): Observable<Destination[]> {
    const url = featuredOnly
      ? `${this.base}/destinations?featured=1`
      : `${this.base}/destinations`;
    return this.http.get<Destination[]>(url);
  }

  getDestination(id: number): Observable<Destination> {
    return this.http.get<Destination>(`${this.base}/destinations/${id}`);
  }

  submitContact(payload: ContactPayload): Observable<ApiResponse<unknown>> {
    return this.http.post<ApiResponse<unknown>>(`${this.base}/contact`, payload);
  }

  createBooking(payload: BookingPayload): Observable<ApiResponse<unknown>> {
    return this.http.post<ApiResponse<unknown>>(`${this.base}/bookings`, payload);
  }

  subscribeNewsletter(email: string): Observable<ApiResponse<unknown>> {
    return this.http.post<ApiResponse<unknown>>(`${this.base}/newsletter`, { email });
  }
}
