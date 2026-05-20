export interface Destination {
  id: number;
  name: string;
  era: string;
  yearLabel: string;
  shortDescription: string;
  description: string;
  priceInr: number;
  durationDays: number;
  difficulty: string;
  imageEmoji: string;
  accentColor: string;
  highlights: string[];
  isFeatured: boolean;
}

export interface ContactPayload {
  name: string;
  email: string;
  phone?: string;
  subject?: string;
  message: string;
}

export interface BookingPayload {
  destinationId: number;
  fullName: string;
  email: string;
  phone: string;
  travelers: number;
  travelDate: string;
  notes?: string;
}

export interface ApiResponse<T> {
  ok?: boolean;
  message?: string;
  data?: T;
  error?: string;
  fields?: { [key: string]: string };
}
