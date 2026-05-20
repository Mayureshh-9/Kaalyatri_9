import { Component } from '@angular/core';

@Component({
  selector: 'app-time-portal',
  template: `
    <div class="portal-wrap">
      <div class="ring ring-1"></div>
      <div class="ring ring-2"></div>
      <div class="ring ring-3"></div>
      <div class="core">
        <span class="core-glyph">∞</span>
      </div>
      <div class="orbit">
        <span class="dot d1"></span>
        <span class="dot d2"></span>
        <span class="dot d3"></span>
      </div>
    </div>
  `,
  styleUrls: ['./time-portal.component.scss'],
})
export class TimePortalComponent {}
