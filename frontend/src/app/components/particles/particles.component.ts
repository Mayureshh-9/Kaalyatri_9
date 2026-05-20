import {
  AfterViewInit,
  Component,
  ElementRef,
  HostListener,
  OnDestroy,
  ViewChild,
} from '@angular/core';

interface Star {
  x: number;
  y: number;
  z: number;
  r: number;
  vx: number;
  vy: number;
  hue: number;
}

interface ShootingStar {
  x: number;
  y: number;
  vx: number;
  vy: number;
  life: number; // 0..1
}

@Component({
  selector: 'app-particles',
  template: `<canvas #c class="particles"></canvas>`,
  styles: [`
    .particles {
      position: fixed;
      inset: 0;
      width: 100%;
      height: 100%;
      z-index: -1;
      pointer-events: none;
      display: block;
    }
  `],
})
export class ParticlesComponent implements AfterViewInit, OnDestroy {
  @ViewChild('c', { static: true }) canvasRef!: ElementRef<HTMLCanvasElement>;

  private ctx!: CanvasRenderingContext2D;
  private stars: Star[] = [];
  private shooting: ShootingStar[] = [];
  private nextShootingAt = 0;
  private rafId = 0;
  private mouse = { x: 0, y: 0 };
  private dpr = window.devicePixelRatio || 1;

  ngAfterViewInit(): void {
    const canvas = this.canvasRef.nativeElement;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;
    this.ctx = ctx;
    this.resize();
    this.spawn();
    this.scheduleNextShooting();
    this.loop();
  }

  ngOnDestroy(): void {
    cancelAnimationFrame(this.rafId);
  }

  @HostListener('window:resize')
  onResize(): void {
    this.resize();
    this.spawn();
  }

  @HostListener('window:mousemove', ['$event'])
  onMouseMove(e: MouseEvent): void {
    this.mouse.x = (e.clientX / window.innerWidth - 0.5) * 2;
    this.mouse.y = (e.clientY / window.innerHeight - 0.5) * 2;
  }

  private resize(): void {
    const canvas = this.canvasRef.nativeElement;
    canvas.width = window.innerWidth * this.dpr;
    canvas.height = window.innerHeight * this.dpr;
    canvas.style.width = window.innerWidth + 'px';
    canvas.style.height = window.innerHeight + 'px';
    this.ctx.scale(this.dpr, this.dpr);
  }

  private spawn(): void {
    const w = window.innerWidth;
    const h = window.innerHeight;
    const target = Math.min(120, Math.floor((w * h) / 14000));
    this.stars = [];
    for (let i = 0; i < target; i++) {
      this.stars.push({
        x: Math.random() * w,
        y: Math.random() * h,
        z: Math.random() * 0.8 + 0.2,
        r: Math.random() * 1.4 + 0.3,
        vx: (Math.random() - 0.5) * 0.12,
        vy: (Math.random() - 0.5) * 0.12,
        hue: 38 + Math.random() * 16,
      });
    }
  }

  private scheduleNextShooting(): void {
    // next shooting star in 3–9 seconds
    this.nextShootingAt = performance.now() + 3000 + Math.random() * 6000;
  }

  private spawnShootingStar(): void {
    const w = window.innerWidth;
    const h = window.innerHeight;
    // Start somewhere in the upper half, fly down-right or down-left
    const fromLeft = Math.random() < 0.5;
    const x = fromLeft ? -50 : w + 50;
    const y = Math.random() * h * 0.5;
    const speed = 12 + Math.random() * 6;
    const vx = (fromLeft ? 1 : -1) * speed;
    const vy = speed * (0.4 + Math.random() * 0.3);
    this.shooting.push({ x, y, vx, vy, life: 1 });
  }

  private loop = (): void => {
    const w = window.innerWidth;
    const h = window.innerHeight;
    const ctx = this.ctx;
    ctx.clearRect(0, 0, w, h);

    // subtle nebula glow that follows cursor slightly
    const grad = ctx.createRadialGradient(
      w / 2 + this.mouse.x * 80,
      h / 2 + this.mouse.y * 80,
      40,
      w / 2,
      h / 2,
      Math.max(w, h),
    );
    grad.addColorStop(0, 'rgba(245, 197, 66, 0.05)');
    grad.addColorStop(1, 'rgba(0, 0, 0, 0)');
    ctx.fillStyle = grad;
    ctx.fillRect(0, 0, w, h);

    // ---- background stars ----
    for (const s of this.stars) {
      s.x += s.vx + this.mouse.x * 0.4 * s.z;
      s.y += s.vy + this.mouse.y * 0.4 * s.z;
      if (s.x < -10) s.x = w + 10;
      if (s.x > w + 10) s.x = -10;
      if (s.y < -10) s.y = h + 10;
      if (s.y > h + 10) s.y = -10;

      const alpha = 0.35 + Math.sin(performance.now() / 800 + s.x) * 0.25;
      ctx.beginPath();
      ctx.fillStyle = `hsla(${s.hue}, 75%, 65%, ${alpha * s.z})`;
      ctx.arc(s.x, s.y, s.r * s.z, 0, Math.PI * 2);
      ctx.fill();
    }

    // connect close stars with subtle gold lines
    for (let i = 0; i < this.stars.length; i++) {
      for (let j = i + 1; j < this.stars.length; j++) {
        const a = this.stars[i];
        const b = this.stars[j];
        const dx = a.x - b.x;
        const dy = a.y - b.y;
        const d2 = dx * dx + dy * dy;
        if (d2 < 110 * 110) {
          ctx.strokeStyle = `rgba(245, 197, 66, ${0.06 * (1 - d2 / (110 * 110))})`;
          ctx.lineWidth = 0.5;
          ctx.beginPath();
          ctx.moveTo(a.x, a.y);
          ctx.lineTo(b.x, b.y);
          ctx.stroke();
        }
      }
    }

    // ---- shooting stars ----
    const now = performance.now();
    if (now > this.nextShootingAt) {
      this.spawnShootingStar();
      this.scheduleNextShooting();
    }

    this.shooting = this.shooting.filter((s) => s.life > 0);
    for (const s of this.shooting) {
      s.x += s.vx;
      s.y += s.vy;
      s.life -= 0.012;

      const tailLen = 90;
      const tx = s.x - s.vx * (tailLen / Math.hypot(s.vx, s.vy));
      const ty = s.y - s.vy * (tailLen / Math.hypot(s.vx, s.vy));

      const tail = ctx.createLinearGradient(s.x, s.y, tx, ty);
      tail.addColorStop(0, `rgba(255, 230, 140, ${0.9 * s.life})`);
      tail.addColorStop(1, `rgba(245, 197, 66, 0)`);
      ctx.strokeStyle = tail;
      ctx.lineWidth = 2;
      ctx.lineCap = 'round';
      ctx.beginPath();
      ctx.moveTo(s.x, s.y);
      ctx.lineTo(tx, ty);
      ctx.stroke();

      ctx.beginPath();
      ctx.fillStyle = `rgba(255, 245, 190, ${0.95 * s.life})`;
      ctx.arc(s.x, s.y, 2.4, 0, Math.PI * 2);
      ctx.fill();
    }

    this.rafId = requestAnimationFrame(this.loop);
  };
}
