import { Component, OnInit, OnDestroy, HostListener } from '@angular/core';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';
import { Pipe, PipeTransform } from '@angular/core';

// ── Interfaces ────────────────────────────────────────────
export interface Destination {
  id: number;
  name: string;
  location: string;
  category: string;
  price: string;
  rating: number;
  duration: string;
  imageUrl: string;
  description: string;
}

export interface FilterChip {
  id: string;
  label: string;
}

export interface Stat {
  label: string;
  current: number;
  target: number;
  suffix: string;
}

export interface CalendarDay {
  date: number;
  disabled: boolean;
  selected: boolean;
  fullDate: Date;
}

export interface Faq {
  q: string;
  a: string;
  open: boolean;
}

export interface Step {
  title: string;
  text: string;
  svgPath: string;
}

export interface Feature {
  title: string;
  text: string;
  svgPath: string;
}

// ── SafeHtml Pipe ─────────────────────────────────────────
@Pipe({ name: 'safeHtml' })
export class SafeHtmlPipe implements PipeTransform {
  constructor(private sanitizer: DomSanitizer) {}
  transform(value: string): SafeHtml {
    return this.sanitizer.bypassSecurityTrustHtml(value);
  }
}

// ── Component ─────────────────────────────────────────────
@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit, OnDestroy {

  // ── Nav ──────────────────────────────────────────────────
  mobileMenuOpen = false;

  // ── Hero slideshow ───────────────────────────────────────
  heroSlideIndex = 0;
  private slideTimer: any;
  heroSlides = [
    { img: 'https://images.unsplash.com/photo-1524492412937-b28074a5d7da?w=1800&q=85' },  // Taj Mahal
    { img: 'https://images.unsplash.com/photo-1626621341517-bbf3d9990a23?w=1800&q=85' },  // Kedarnath
    { img: 'https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?w=1800&q=85' },  // Kerala
    { img: 'https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?w=1800&q=85' },  // Goa
  ];

  // ── Search ───────────────────────────────────────────────
  selectedDestination: Destination | null = null;
  travellersCount = 2;
  selectedDate: Date | null = null;
  selectedDateFormatted = '';
  calendarOpen = false;

  // ── Calendar ─────────────────────────────────────────────
  currentYear  = new Date().getFullYear();
  currentMonth = new Date().getMonth();
  calendarDays: CalendarDay[] = [];

  // ── Filters ──────────────────────────────────────────────
  activeFilter = 'all';
  filterChips: FilterChip[] = [
    { id: 'all',      label: 'All Destinations' },
    { id: 'dham',     label: '4 Dham Yatra'     },
    { id: 'beach',    label: 'Beaches'           },
    { id: 'heritage', label: 'Heritage'          },
    { id: 'hill',     label: 'Hill Stations'     },
  ];

  // ── Destinations ─────────────────────────────────────────
  destinations: Destination[] = [
    {
      id: 1, name: 'Kedarnath', location: 'Uttarakhand', category: 'dham',
      price: '₹12,999', rating: 4.9, duration: '4 Days',
      imageUrl: 'https://images.unsplash.com/photo-1626621341517-bbf3d9990a23?w=700&q=80',
      description: 'Sacred Himalayan shrine nestled among snow-capped peaks, part of the revered Char Dham circuit.'
    },
    {
      id: 2, name: 'Badrinath', location: 'Uttarakhand', category: 'dham',
      price: '₹11,999', rating: 4.8, duration: '4 Days',
      imageUrl: 'https://images.unsplash.com/photo-1590577976322-3d2d6a2130f4?w=700&q=80',
      description: 'Ancient temple town on the banks of Alaknanda, surrounded by breathtaking alpine scenery.'
    },
    {
      id: 3, name: 'Dwarka', location: 'Gujarat', category: 'dham',
      price: '₹9,999', rating: 4.7, duration: '3 Days',
      imageUrl: 'https://images.unsplash.com/photo-1567157577867-05ccb1388e66?w=700&q=80',
      description: 'The ancient city of Lord Krishna, one of the four sacred dhams of Hindu pilgrimage.'
    },
    {
      id: 4, name: 'Puri', location: 'Odisha', category: 'dham',
      price: '₹8,999', rating: 4.8, duration: '3 Days',
      imageUrl: 'https://images.unsplash.com/photo-1559592413-7cec4d0cae2b?w=700&q=80',
      description: 'Home to the magnificent Jagannath Temple and pristine golden shores along the Bay of Bengal.'
    },
    {
      id: 5, name: 'Kerala Backwaters', location: 'Kerala', category: 'beach',
      price: '₹15,999', rating: 4.9, duration: '5 Days',
      imageUrl: 'https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?w=700&q=80',
      description: 'Glide through emerald canals on a luxury houseboat surrounded by coconut palms and serenity.'
    },
    {
      id: 6, name: 'Goa Beaches', location: 'Goa', category: 'beach',
      price: '₹12,499', rating: 4.8, duration: '4 Days',
      imageUrl: 'https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?w=700&q=80',
      description: 'Sun-drenched beaches, vibrant nightlife, and centuries of Portuguese colonial heritage.'
    },
    {
      id: 7, name: 'Gokarna', location: 'Karnataka', category: 'beach',
      price: '₹8,999', rating: 4.7, duration: '3 Days',
      imageUrl: 'https://images.unsplash.com/photo-1583309219338-a582f1db9a26?w=700&q=80',
      description: 'A soul-soothing blend of pristine beaches, towering cliffs, and an ancient Shiva temple.'
    },
    {
      id: 8, name: 'Hampi', location: 'Karnataka', category: 'heritage',
      price: '₹9,999', rating: 4.8, duration: '3 Days',
      imageUrl: 'https://images.unsplash.com/photo-1590736704728-f4730bb30770?w=700&q=80',
      description: 'Timeless ruins of the Vijayanagara Empire — a UNESCO World Heritage Site of staggering scale.'
    },
    {
      id: 9, name: 'Jaipur', location: 'Rajasthan', category: 'heritage',
      price: '₹13,999', rating: 4.8, duration: '4 Days',
      imageUrl: 'https://images.unsplash.com/photo-1524230572899-a752b3835840?w=700&q=80',
      description: 'The Pink City — a royal tapestry of amber forts, hawa mahals, and living Rajput traditions.'
    },
    {
      id: 10, name: 'Manali', location: 'Himachal Pradesh', category: 'hill',
      price: '₹11,999', rating: 4.7, duration: '5 Days',
      imageUrl: 'https://images.unsplash.com/photo-1605649487212-47bdab064df7?w=700&q=80',
      description: 'Snow-capped passes, roaring rivers, and thrilling adventures in the heart of the Himalayas.'
    },
    {
      id: 11, name: 'Shimla', location: 'Himachal Pradesh', category: 'hill',
      price: '₹10,999', rating: 4.6, duration: '4 Days',
      imageUrl: 'https://images.unsplash.com/photo-1626714262844-1e99f82b152f?w=700&q=80',
      description: 'The Queen of Hill Stations, known for its Victorian architecture and scenic views over the mountains.'
    },
    {
      id: 12, name: 'Varanasi', location: 'Uttar Pradesh', category: 'heritage',
      price: '₹7,999', rating: 4.7, duration: '3 Days',
      imageUrl: 'https://images.unsplash.com/photo-1559929406-ec2a9f76f40f?w=700&q=80',
      description: 'An ancient city with spiritual significance, famous for its ghats along the sacred Ganges River.'
    }
  ];

  filteredDestinations: Destination[] = [];
  loading = false;

  // ── Statistics ───────────────────────────────────────────
  stats: Stat[] = [
    { label: 'Happy Travelers', current: 0, target: 8500, suffix: '+' },
    { label: 'Destinations', current: 0, target: 50, suffix: '+' },
    { label: 'Years Experience', current: 0, target: 20, suffix: '+' },
    { label: 'Satisfaction', current: 0, target: 99, suffix: '%' }
  ];

  // ── How It Works ────────────────────────────────────────
  steps: Step[] = [
    {
      title: 'Choose your destination',
      text: 'Browse curated trips and pick the place that matches your vibe.',
      svgPath: '<path d="M12 2a7 7 0 0 1 7 7c0 4.9-5.2 10.1-6.5 11.6a1 1 0 0 1-1.5 0C10.2 19.1 5 13.9 5 9a7 7 0 0 1 7-7Z"/><circle cx="12" cy="9" r="2.5"/>'
    },
    {
      title: 'Pick your date',
      text: 'Select a travel date that fits your schedule and plan your journey.',
      svgPath: '<rect x="4" y="5" width="16" height="14" rx="2"/><path d="M8 3v4M16 3v4M4 10h16"/>'
    },
    {
      title: 'Confirm your booking',
      text: 'Review the itinerary, confirm your package, and let us handle the rest.',
      svgPath: '<path d="M5 12.5 10 17l9-9"/>'
    },
    {
      title: 'Travel with ease',
      text: 'Enjoy seamless transfers, stays, and support throughout your trip.',
      svgPath: '<path d="M4 12h16M12 4v16"/>'
    }
  ];

  // ── Features ─────────────────────────────────────────────
  features: Feature[] = [
    { title: 'Safe Travel', text: 'Fully insured trips with 24/7 customer support', svgPath: '' },
    { title: 'Expert Guides', text: 'Local experts who know every hidden gem', svgPath: '' },
    { title: 'Best Hotels', text: 'Handpicked accommodations for your comfort', svgPath: '' },
    { title: 'Best Price', text: 'No hidden charges, price match guaranteed', svgPath: '' },
    { title: 'Private Transfers', text: 'Comfortable vehicles for your journey', svgPath: '' },
    { title: '24/7 Support', text: 'We are always here to help you', svgPath: '' }
  ];

  // ── Testimonials ─────────────────────────────────────────
  testimonials = [
    { name: 'Ramesh Sharma', city: 'Delhi', quote: 'The Kedarnath yatra was beautifully organized. Everything from transport to accommodation was perfect!' },
    { name: 'Priya Nair', city: 'Mumbai', quote: 'Kerala backwaters tour exceeded all expectations. Our guide was amazing and the houseboat stay was magical.' },
    { name: 'Ankit Verma', city: 'Bengaluru', quote: 'Goa trip was fantastic! Great hotel, smooth transfers, and perfect itinerary. Will book again!' }
  ];

  // ── FAQs ─────────────────────────────────────────────────
  faqs: Faq[] = [
    { q: 'How do I book a trip?', a: 'Simply select your destination, travel date, number of travellers, and click "Find My Trip". You will be guided through the booking process.', open: false },
    { q: 'What is included in the package?', a: 'All our packages include accommodation (twin sharing), breakfast, private transfers, guided tours, and 24/7 support. Flight/train tickets are extra unless specified.', open: true },
    { q: 'Can I customize my itinerary?', a: 'Absolutely! Contact our travel consultants to create a personalized itinerary that matches your preferences and budget.', open: false },
    { q: 'What is your cancellation policy?', a: 'Free cancellation up to 15 days before departure. 50% refund between 7-14 days. No refund within 7 days of departure.', open: false },
    { q: 'Do you offer group discounts?', a: 'Yes! Groups of 6 or more receive special discounts. Contact our group travel desk for a custom quote.', open: false },
    { q: 'Do you provide travel insurance?', a: 'We strongly recommend travel insurance. We partner with leading insurers to offer comprehensive coverage options.', open: false }
  ];
galleryImages: any;

  // ── Component Life Cycle ─────────────────────────────────
  ngOnInit() {
    this.applyFilter();
    this.initCalendar();
    this.setupStatsObserver();
    this.startSlideShow();
  }

  ngOnDestroy() {
    clearInterval(this.slideTimer);
  }

  // ── Start Hero Slideshow ─────────────────────────────────
  startSlideShow() {
    this.slideTimer = setInterval(() => {
      this.heroSlideIndex = (this.heroSlideIndex + 1) % this.heroSlides.length;
    }, 5000);
  }

  // ── Stats Animation ────────────────────────────────────
  private statsAnimated = false;

  setupStatsObserver() {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting && !this.statsAnimated) {
          this.statsAnimated = true;
          this.animateStats();
          observer.disconnect();
        }
      });
    }, { threshold: 0.3 });

    setTimeout(() => {
      const statsElement = document.querySelector('.stats-strip');
      if (statsElement) observer.observe(statsElement);
    }, 100);
  }

  animateStats() {
    const duration = 1500;
    const startTime = performance.now();

    const animate = (currentTime: number) => {
      const elapsed = currentTime - startTime;
      const progress = Math.min(1, elapsed / duration);
      const eased = 1 - Math.pow(1 - progress, 3);

      this.stats.forEach(stat => {
        stat.current = Math.floor(stat.target * eased);
      });

      if (progress < 1) {
        requestAnimationFrame(animate);
      } else {
        this.stats.forEach(stat => {
          stat.current = stat.target;
        });
      }
    };

    requestAnimationFrame(animate);
  }

  // ── Filter Logic ────────────────────────────────────────
  setFilter(filterId: string) {
    this.activeFilter = filterId;
    this.applyFilter();
  }

  applyFilter() {
    if (this.activeFilter === 'all') {
      this.filteredDestinations = [...this.destinations];
    } else {
      this.filteredDestinations = this.destinations.filter(d => d.category === this.activeFilter);
    }
  }

  getCountByCategory(categoryId: string): number {
    if (categoryId === 'all') return this.destinations.length;
    return this.destinations.filter(d => d.category === categoryId).length;
  }

  getRatingStars(rating: number): number[] {
    return Array(Math.floor(rating)).fill(0);
  }

  // ── Calendar Functionality ──────────────────────────────
  initCalendar() {
    this.generateCalendarDays();
  }

  generateCalendarDays() {
    const today = new Date();
    today.setHours(0, 0, 0, 0);

    const firstDay = new Date(this.currentYear, this.currentMonth, 1);
    const startDay = firstDay.getDay();
    const daysInMonth = new Date(this.currentYear, this.currentMonth + 1, 0).getDate();

    const days: CalendarDay[] = [];

    // Add empty cells for start of month
    for (let i = 0; i < startDay; i++) {
      days.push({ date: 0, disabled: true, selected: false, fullDate: new Date() });
    }

    // Add actual days
    for (let d = 1; d <= daysInMonth; d++) {
      const cellDate = new Date(this.currentYear, this.currentMonth, d);
      const isDisabled = cellDate < today;
      const isSelected = !!this.selectedDate && cellDate.toDateString() === this.selectedDate.toDateString();
      days.push({
        date: d,
        disabled: isDisabled,
        selected: isSelected,
        fullDate: cellDate
      });
    }

    this.calendarDays = days;
  }

  get currentMonthName(): string {
    const monthNames = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
    return monthNames[this.currentMonth];
  }

  prevMonth() {
    this.currentMonth--;
    if (this.currentMonth < 0) {
      this.currentMonth = 11;
      this.currentYear--;
    }
    this.generateCalendarDays();
  }

  nextMonth() {
    this.currentMonth++;
    if (this.currentMonth > 11) {
      this.currentMonth = 0;
      this.currentYear++;
    }
    this.generateCalendarDays();
  }

  selectDate(day: CalendarDay) {
    if (day.disabled || day.date === 0) return;

    this.selectedDate = new Date(this.currentYear, this.currentMonth, day.date);
    this.selectedDateFormatted = this.selectedDate.toLocaleDateString('en-IN', {
      day: 'numeric',
      month: 'short',
      year: 'numeric'
    });
    this.calendarOpen = false;
    this.generateCalendarDays();
  }

  toggleCalendar() {
    this.calendarOpen = !this.calendarOpen;
    if (this.calendarOpen) {
      this.generateCalendarDays();
    }
  }

  @HostListener('document:click', ['$event'])
  onDocumentClick(event: MouseEvent) {
    const target = event.target as HTMLElement;
    if (!target.closest('.datepicker-wrapper')) {
      this.calendarOpen = false;
    }
  }

  // ── Search ───────────────────────────────────────────────
  onDestinationChange() {
    // Optional: Auto-populate price or other details when destination is selected
  }

  search() {
    if (!this.selectedDestination) {
      alert('Please select a destination');
      return;
    }
    if (!this.selectedDate) {
      alert('Please select a travel date');
      return;
    }

    alert(`🔍 Searching for ${this.selectedDestination.name}\n👥 ${this.travellersCount} travellers\n📅 ${this.selectedDateFormatted}\n\nOur team will contact you shortly with the best options!`);
  }

  viewDestination(destination: Destination) {
    alert(`📍 ${destination.name}\n\n${destination.description}\n💰 ${destination.price} per person\n📅 ${destination.duration}\n⭐ Rating: ${destination.rating}/5\n\nContact us to book this amazing journey!`);
  }

  scrollToSearch() {
    const searchCard = document.querySelector('.search-card');
    searchCard?.scrollIntoView({ behavior: 'smooth', block: 'center' });
  }

  contactUs() {
    alert('📞 Call us: +91 98765 43210\n✉️ Email: hello@kaalyatri.com\n\nWe\'d love to help you plan your journey!');
  }

  toggleFaq(index: number) {
    this.faqs[index].open = !this.faqs[index].open;
  }
}
