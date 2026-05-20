import { Component } from '@angular/core';

@Component({
  selector: 'app-about',
  templateUrl: './about.component.html',
  styleUrls: ['./about.component.scss'],
})
export class AboutComponent {
  milestones = [
    { year: '2026', title: 'KaalYatri started',          text: 'Common Convis opened the world\'s first time travel agency in Mumbai.' },
    { year: '2027', title: 'Our first trip',             text: 'Six guests had dinner with Akbar in 1582. Everyone came home safe and happy.' },
    { year: '2029', title: '100 places ready',           text: 'From the Indus Valley to the Apollo Moon landing. Insurance partner: Lloyd\'s of London.' },
    { year: '2031', title: 'Mars 2174 trip opened',      text: 'We started future trips with the New Olympus Mars colony.' },
    { year: '2033', title: 'Clean energy time machines', text: 'All our trips now run on clean, recycled time energy.' },
  ];

  team = [
    { name: 'Common Convis', role: 'Founder & Chief Time Traveller', emoji: '🧭' },
    { name: 'Dr. Aanya Rao', role: 'Head of History Research',        emoji: '📜' },
    { name: 'Marc Liu',      role: 'Lead Engineer',                   emoji: '⚙️' },
    { name: 'Zara Ahmed',    role: 'Guest Experience',                emoji: '✨' },
  ];
}
