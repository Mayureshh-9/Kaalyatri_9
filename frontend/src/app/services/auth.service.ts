import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable, of } from 'rxjs';
import { tap, catchError } from 'rxjs/operators';
import { environment } from '../../environments/environment';
import { User, ApiResponse } from '../models/destination.model';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private readonly base = environment.apiBaseUrl;
  private currentUserSubject = new BehaviorSubject<User | null>(this.getStoredUser());
  public currentUser$ = this.currentUserSubject.asObservable();

  constructor(private http: HttpClient) {
    if (this.getToken()) {
      this.fetchProfile().subscribe();
    }
  }

  get currentUserValue(): User | null {
    return this.currentUserSubject.value;
  }

  getToken(): string | null {
    return localStorage.getItem('ky_access_token');
  }

  private getStoredUser(): User | null {
    const raw = localStorage.getItem('ky_user');
    return raw ? JSON.parse(raw) : null;
  }

  register(payload: any): Observable<ApiResponse<any>> {
    return this.http.post<ApiResponse<any>>(`${this.base}/auth/register`, payload).pipe(
      tap(res => {
        if (res.access_token && res.user) {
          this.setSession(res.access_token, res.user);
        }
      })
    );
  }

  login(payload: any): Observable<ApiResponse<any>> {
    return this.http.post<ApiResponse<any>>(`${this.base}/auth/login`, payload).pipe(
      tap(res => {
        if (res.access_token && res.user) {
          this.setSession(res.access_token, res.user);
        }
      })
    );
  }

  fetchProfile(): Observable<any> {
    return this.http.get<any>(`${this.base}/auth/me`).pipe(
      tap(res => {
        if (res.data) {
          localStorage.setItem('ky_user', JSON.stringify(res.data));
          this.currentUserSubject.next(res.data);
        }
      }),
      catchError(() => {
        this.logout();
        return of(null);
      })
    );
  }

  logout(): void {
    localStorage.removeItem('ky_access_token');
    localStorage.removeItem('ky_user');
    this.currentUserSubject.next(null);
  }

  private setSession(token: string, user: User): void {
    localStorage.setItem('ky_access_token', token);
    localStorage.setItem('ky_user', JSON.stringify(user));
    this.currentUserSubject.next(user);
  }
}
