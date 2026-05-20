import { Directive, ElementRef, HostListener } from '@angular/core';

@Directive({ selector: '[appTilt]' })
export class TiltDirective {
  private readonly max = 10;

  constructor(private el: ElementRef<HTMLElement>) {
    const style = el.nativeElement.style;
    style.transformStyle = 'preserve-3d';
    style.transition = 'transform 0.25s ease';
    style.willChange = 'transform';
  }

  @HostListener('mousemove', ['$event'])
  onMove(e: MouseEvent): void {
    const node = this.el.nativeElement;
    const rect = node.getBoundingClientRect();
    const x = (e.clientX - rect.left) / rect.width - 0.5;
    const y = (e.clientY - rect.top) / rect.height - 0.5;
    const rotY = x * this.max;
    const rotX = -y * this.max;
    node.style.transform = `perspective(900px) rotateX(${rotX}deg) rotateY(${rotY}deg) translateY(-4px)`;
  }

  @HostListener('mouseleave')
  onLeave(): void {
    this.el.nativeElement.style.transform = 'perspective(900px) rotateX(0) rotateY(0) translateY(0)';
  }
}
