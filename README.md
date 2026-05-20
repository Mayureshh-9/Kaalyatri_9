# KaalYatri — The Time Travellers

A full-stack tourism website for **KaalYatri**, India's first chronotourism agency.
*Journeys Beyond Destinations.*

- **Frontend:** Angular 17 (TypeScript, SCSS, reactive forms, custom animations)
- **Backend:** Python (Flask + Flask-SQLAlchemy + Flask-CORS)
- **Database:** PostgreSQL
- **APIs:** Destinations, Contact, Bookings, Newsletter

```
KaalYatri/
├── backend/        # Python Flask REST API
├── frontend/       # Angular 17 SPA
└── README.md
```

---

## 1. Prerequisites

| Tool | Version |
|---|---|
| Python | 3.10+ |
| Node.js | 18+ |
| Angular CLI | 17+ (`npm i -g @angular/cli`) |
| PostgreSQL | 14+ running locally |

---

## 2. Database setup

Create the database (one-time):

```bash
psql -U postgres -c "CREATE DATABASE kaalyatri;"
```

---

## 3. Backend — Python Flask API

```bash
cd backend

# create virtual environment
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

# install deps
pip install -r requirements.txt

# environment
cp .env.example .env
# edit .env and set DATABASE_URL to your local postgres

# create tables + seed sample destinations
python seed.py

# run dev server (http://localhost:5000)
python app.py
```

### REST endpoints

| Method | Path | Purpose |
|---|---|---|
| GET  | `/api/health`                  | health check |
| GET  | `/api/company`                 | company info |
| GET  | `/api/destinations`            | list all (or `?featured=1`) |
| GET  | `/api/destinations/<id>`       | single destination |
| POST | `/api/contact`                 | submit a contact-form message |
| GET  | `/api/contact`                 | (admin) list messages |
| POST | `/api/bookings`                | create a booking |
| GET  | `/api/bookings`                | (admin) list bookings |
| POST | `/api/newsletter`              | subscribe to newsletter |

### Contact API example

```bash
curl -X POST http://localhost:5000/api/contact \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Aarav Sharma",
    "email": "aarav@example.com",
    "phone": "+91 9876543210",
    "subject": "Custom voyage to 1947",
    "message": "Can you arrange a private trip to witness Indian Independence?"
  }'
```

### Booking API example

```bash
curl -X POST http://localhost:5000/api/bookings \
  -H "Content-Type: application/json" \
  -d '{
    "destinationId": 1,
    "fullName": "Aarav Sharma",
    "email": "aarav@example.com",
    "phone": "+91 9876543210",
    "travelers": 2,
    "travelDate": "2026-09-15",
    "notes": "Vegetarian meals please"
  }'
```

---

## 4. Frontend — Angular

```bash
cd frontend

# install deps
npm install

# run dev server (http://localhost:4200)
npm start
```

The frontend talks to `http://localhost:5000/api` by default. Override in
`frontend/src/environments/environment.ts`.

---

## 5. Pages

| Route | Description |
|---|---|
| `/`                    | Animated hero, featured destinations, features grid, how-it-works, testimonials, CTA |
| `/destinations`        | Searchable + filterable grid of all eras |
| `/destinations/:id`    | Detail view with highlights and book CTA |
| `/about`               | Manifesto, timeline, team |
| `/contact`             | Contact form (POSTs to `/api/contact`) |
| `/book` and `/book/:id`| Booking form with live trip summary |

---

## 6. Interactive design highlights

- Animated **starfield + nebula canvas** background that reacts to the cursor.
- **Time portal** SVG/CSS animation in the hero (rotating rings, orbiting dots, pulsing core).
- **Scroll-reveal** directive (`appReveal`) — sections fade up as they enter the viewport.
- **3D tilt** directive (`appTilt`) — destination cards tilt with the cursor.
- **Glassmorphism + cosmic gradient** theme (purple → cyan → pink).
- Reactive forms with **inline + server-side validation** feedback.

---

## 7. Production builds

```bash
# Backend
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# Frontend
cd frontend
npm run build      # outputs to frontend/dist/kaalyatri
```

Serve `frontend/dist/kaalyatri/browser` from any static host (Nginx, Vercel,
Netlify) and reverse-proxy `/api` to the Flask backend.

---

## 8. Owner

**Common Convis** — `abc@gmail.com`
Founder & Chrononaut-in-Chief, KaalYatri Time Tourism Pvt. Ltd.
