from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Destination(db.Model):
    __tablename__ = "destinations"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    era = db.Column(db.String(100), nullable=False)
    year_label = db.Column(db.String(50), nullable=False)
    short_description = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price_inr = db.Column(db.Numeric(12, 2), nullable=False)
    duration_days = db.Column(db.Integer, nullable=False, default=7)
    difficulty = db.Column(db.String(50), default="Moderate")
    image_emoji = db.Column(db.String(20), default="🌍")
    accent_color = db.Column(db.String(20), default="#7c4dff")
    highlights = db.Column(db.Text)
    is_featured = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "era": self.era,
            "yearLabel": self.year_label,
            "shortDescription": self.short_description,
            "description": self.description,
            "priceInr": float(self.price_inr),
            "durationDays": self.duration_days,
            "difficulty": self.difficulty,
            "imageEmoji": self.image_emoji,
            "accentColor": self.accent_color,
            "highlights": (self.highlights or "").split("|") if self.highlights else [],
            "isFeatured": self.is_featured,
        }


class ContactMessage(db.Model):
    __tablename__ = "contact_messages"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(30))
    subject = db.Column(db.String(200))
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "subject": self.subject,
            "message": self.message,
            "isRead": self.is_read,
            "createdAt": self.created_at.isoformat() if self.created_at else None,
        }


class Booking(db.Model):
    __tablename__ = "bookings"

    id = db.Column(db.Integer, primary_key=True)
    destination_id = db.Column(db.Integer, db.ForeignKey("destinations.id"), nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(30), nullable=False)
    travelers = db.Column(db.Integer, nullable=False, default=1)
    travel_date = db.Column(db.Date, nullable=False)
    notes = db.Column(db.Text)
    status = db.Column(db.String(30), default="pending")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    destination = db.relationship("Destination", backref="bookings")

    def to_dict(self):
        return {
            "id": self.id,
            "destinationId": self.destination_id,
            "destinationName": self.destination.name if self.destination else None,
            "fullName": self.full_name,
            "email": self.email,
            "phone": self.phone,
            "travelers": self.travelers,
            "travelDate": self.travel_date.isoformat() if self.travel_date else None,
            "notes": self.notes,
            "status": self.status,
            "createdAt": self.created_at.isoformat() if self.created_at else None,
        }


class NewsletterSubscriber(db.Model):
    __tablename__ = "newsletter_subscribers"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "createdAt": self.created_at.isoformat() if self.created_at else None,
        }
