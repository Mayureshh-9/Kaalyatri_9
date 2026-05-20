import { Component, OnDestroy, OnInit } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
})
export class AppComponent implements OnInit, OnDestroy {
  title = 'KaalYatri';

  showGreeting = false;
  greetingClosing = false;
  private autoDismissTimer?: ReturnType<typeof setTimeout>;

  ngOnInit(): void {
    const greeted = sessionStorage.getItem('kaalyatri_greeted');
    if (!greeted) {
      // small delay so the page settles before the greeting slides in
      setTimeout(() => {
        this.showGreeting = true;
        sessionStorage.setItem('kaalyatri_greeted', '1');
        this.autoDismissTimer = setTimeout(() => this.dismissGreeting(), 9000);
      }, 800);
    }
  }

  ngOnDestroy(): void {
    if (this.autoDismissTimer) clearTimeout(this.autoDismissTimer);
  }

  dismissGreeting(): void {
    if (this.autoDismissTimer) {
      clearTimeout(this.autoDismissTimer);
      this.autoDismissTimer = undefined;
    }
    this.greetingClosing = true;
    setTimeout(() => {
      this.showGreeting = false;
      this.greetingClosing = false;
    }, 350);
  }
}
