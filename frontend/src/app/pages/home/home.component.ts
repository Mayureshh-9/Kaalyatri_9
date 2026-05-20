import { AfterViewInit, Component, ElementRef, HostListener, OnDestroy, OnInit, ViewChild } from '@angular/core';
import { Router } from '@angular/router';
import { ApiService } from '../../services/api.service';
import { Destination } from '../../models/destination.model';

interface CounterStat {
  label: string;
  target: number;
  current: number;
}

type EraCategory = 'all' | 'ancient' | 'classic' | 'modern' | 'future';

interface EraChip {
  id: EraCategory;
  label: string;
  emoji: string;
}

interface Slide {
  emoji: string;
  era: string;
  year: string;
  title: string;
  text: string;
  accent: string;
}

interface Faq {
  q: string;
  a: string;
  open: boolean;
}

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss'],
})
export class HomeComponent implements OnInit, AfterViewInit, OnDestroy {
  destinations: Destination[] = [];
  filtered: Destination[] = [];
  loading = true;
  apiOffline = false;

  /* ---------- Search widget ---------- */
  searchDestinationId: number | null = null;
  searchTravellers = 2;
  searchDate = '';
  minDate = '';

  /* ---------- Era category filter ---------- */
  activeEra: EraCategory = 'all';
  eraChips: EraChip[] = [
    { id: 'all',     label: 'All Trips', emoji: '🌍' },
    { id: 'ancient', label: 'Ancient',   emoji: '🏺' },
    { id: 'classic', label: 'Classic',   emoji: '🏰' },
    { id: 'modern',  label: 'Modern',    emoji: '🎩' },
    { id: 'future',  label: 'Future',    emoji: '🚀' },
  ];

  /* ---------- Static content ---------- */
  features = [
    { icon: '🛡️', title: 'Safe Trips',     text: 'Every journey is fully insured. Our trained guides keep you safe.' },
    { icon: '🧭', title: 'Expert Guides',  text: 'History teachers and scientists travel with you to every place.' },
    { icon: '🌐', title: 'Easy Talking',   text: 'A small earpiece lets you understand and speak any language.' },
    { icon: '🪶', title: 'Period Clothes', text: 'We give you clothes from that time so you blend in with the locals.' },
    { icon: '⏱️', title: 'Quick Return',   text: 'You come back home just five minutes after you left.' },
    { icon: '🎟️', title: 'No Visa Needed', text: 'No paperwork, no airports, no queues. Just step in and go.' },
  ];

  testimonials = [
    { name: 'Aarav S.',  role: 'Mumbai',     emoji: '🚂', stars: 5, quote: 'I had dinner with Akbar! KaalYatri made it easy and safe.' },
    { name: 'Priya M.',  role: 'Bengaluru',  emoji: '✈️', stars: 5, quote: 'I saw the Wright Brothers fly. Cried all the way back home.' },
    { name: 'Marcus L.', role: 'Singapore',  emoji: '🚢', stars: 5, quote: 'The Mars Colony 2174 trip was the best holiday of my life.' },
  ];

  stats: CounterStat[] = [
    { label: 'Travellers',    target: 12480, current: 0 },
    { label: 'Time periods',  target: 87,    current: 0 },
    { label: 'Years covered', target: 24000, current: 0 },
    { label: 'Accidents',     target: 0,     current: 0 },
  ];

  /* ---------- Slideshow ---------- */
  slides: Slide[] = [
    { emoji: '🏜️', era: 'Ancient Egypt', year: '2560 BCE', title: 'Watch the Great Pyramid rise',     text: 'Stand on the banks of the Nile while masons place the final stones of Khufu\'s pyramid.', accent: '#f5b400' },
    { emoji: '🎨', era: 'Renaissance',    year: '1503 CE',  title: 'Sip wine with Da Vinci',          text: 'Walk the streets of Florence, visit Leonardo\'s workshop, and watch him sketch the Mona Lisa.', accent: '#c9356b' },
    { emoji: '🕌', era: 'Mughal Agra',    year: '1648 CE',  title: 'See the Taj Mahal newly built',   text: 'The marble is still bright. Meet artisans from Persia and ride a royal elephant.', accent: '#26c2a8' },
    { emoji: '🦖', era: 'Cretaceous',     year: '66M BCE',  title: 'Float over a dinosaur valley',    text: 'A safe hover-pod takes you above nesting hadrosaurs and stalking T. Rex.', accent: '#5cb85c' },
    { emoji: '🪐', era: 'Mars Colony',    year: '2174 CE',  title: 'Walk on the red planet',          text: 'Tour New Olympus city, take the maglev to Olympus Mons, attend a zero-G concert.', accent: '#ff5470' },
  ];
  slideIndex = 0;
  private slideTimer?: ReturnType<typeof setInterval>;

  /* ---------- FAQ ---------- */
  faqs: Faq[] = [
    { q: 'Is time travel safe?',
      a: 'Yes. Every trip is fully insured and led by trained guides. We have completed over 12,000 trips with zero accidents.',
      open: true },
    { q: 'How long does a trip really take?',
      a: 'From your point of view, a trip lasts 4 to 9 days. But you return home just five minutes after you left.',
      open: false },
    { q: 'What should I wear?',
      a: 'Don\'t worry — we give you proper clothes for every time period, so you blend in safely with the locals.',
      open: false },
    { q: 'Can I bring my phone or camera?',
      a: 'You can bring them, but they will not have signal in the past! We give you a memory journal you can keep.',
      open: false },
    { q: 'How much does a trip cost?',
      a: 'Trips start at ₹1,34,999 per person. The price depends on the time period and how many days you go for.',
      open: false },
    { q: 'Can children come on trips?',
      a: 'Yes, children above 12 years are welcome with a parent. We run special family trips during school holidays.',
      open: false },
    { q: 'Do I need a passport or visa?',
      a: 'No paperwork at all. Time is our only border. Just bring a valid ID and arrive on the day of your trip.',
      open: false },
  ];

  /* ---------- Parallax ---------- */
  parallaxX = 0;
  parallaxY = 0;

  @ViewChild('hero') heroRef?: ElementRef<HTMLElement>;
  private countersStarted = false;

  constructor(private api: ApiService, private router: Router) {
    const tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate() + 1);
    this.minDate = tomorrow.toISOString().split('T')[0];
    this.searchDate = this.minDate;
  }

  ngOnInit(): void {
    this.api.getDestinations().subscribe({
      next: (items) => {
        this.destinations = items;
        this.applyFilter();
        this.loading = false;
      },
      error: () => {
        this.loading = false;
        this.apiOffline = true;
      },
    });

    this.startSlideshow();
  }

  ngOnDestroy(): void {
    this.stopSlideshow();
  }

  ngAfterViewInit(): void {
    const observer = new IntersectionObserver(
      (entries) => {
        for (const entry of entries) {
          if (entry.isIntersecting && !this.countersStarted) {
            this.countersStarted = true;
            this.runCounters();
            observer.disconnect();
            break;
          }
        }
      },
      { threshold: 0.4 },
    );
    setTimeout(() => {
      const node = document.querySelector('.stats-strip');
      if (node) observer.observe(node);
    }, 0);
  }

  /* ---------- Era filter ---------- */
  setEra(id: EraCategory): void {
    this.activeEra = id;
    this.applyFilter();
  }

  applyFilter(): void {
    if (this.activeEra === 'all') {
      this.filtered = this.destinations.slice(0, 6);
      return;
    }
    this.filtered = this.destinations
      .filter((d) => this.categoryOf(d) === this.activeEra)
      .slice(0, 6);
  }

  countIn(id: EraCategory): number {
    if (id === 'all') return this.destinations.length;
    return this.destinations.filter((d) => this.categoryOf(d) === id).length;
  }

  private categoryOf(d: Destination): EraCategory {
    const label = (d.yearLabel || '').toUpperCase();
    if (label.includes('BCE') || label.includes('M ')) return 'ancient';
    const num = parseInt(label.replace(/[^0-9]/g, ''), 10) || 0;
    if (num < 1800) return 'classic';
    if (num < 2026) return 'modern';
    return 'future';
  }

  /* ---------- Search widget ---------- */
  search(): void {
    if (this.searchDestinationId) {
      this.router.navigate(['/book', this.searchDestinationId]);
    } else {
      this.router.navigate(['/destinations']);
    }
  }

  /* ---------- Slideshow ---------- */
  startSlideshow(): void {
    this.stopSlideshow();
    this.slideTimer = setInterval(() => this.nextSlide(), 4500);
  }
  stopSlideshow(): void {
    if (this.slideTimer) clearInterval(this.slideTimer);
    this.slideTimer = undefined;
  }
  nextSlide(): void { this.slideIndex = (this.slideIndex + 1) % this.slides.length; }
  prevSlide(): void { this.slideIndex = (this.slideIndex - 1 + this.slides.length) % this.slides.length; }
  goToSlide(i: number): void { this.slideIndex = i; this.startSlideshow(); }

  /* ---------- FAQ ---------- */
  toggleFaq(faq: Faq): void {
    const wasOpen = faq.open;
    this.faqs.forEach((f) => (f.open = false));
    faq.open = !wasOpen;
  }

  /* ---------- Hero parallax ---------- */
  @HostListener('mousemove', ['$event'])
  onMouseMove(e: MouseEvent): void {
    const node = this.heroRef?.nativeElement;
    if (!node) return;
    const rect = node.getBoundingClientRect();
    if (
      e.clientY < rect.top ||
      e.clientY > rect.bottom ||
      e.clientX < rect.left ||
      e.clientX > rect.right
    ) {
      this.parallaxX = 0;
      this.parallaxY = 0;
      return;
    }
    const px = (e.clientX - rect.left) / rect.width - 0.5;
    const py = (e.clientY - rect.top) / rect.height - 0.5;
    this.parallaxX = px * 24;
    this.parallaxY = py * 24;
  }

  /* ---------- Animated counters ---------- */
  private runCounters(): void {
    const duration = 1600;
    const start = performance.now();
    const tick = (now: number): void => {
      const t = Math.min(1, (now - start) / duration);
      const eased = 1 - Math.pow(1 - t, 3);
      this.stats = this.stats.map((s) => ({ ...s, current: Math.round(s.target * eased) }));
      if (t < 1) requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
  }

  formatStat(s: CounterStat): string {
    return s.current.toLocaleString('en-IN');
  }

  formatPrice(p: number): string {
    return '₹' + p.toLocaleString('en-IN');
  }
}
