from datetime import datetime
import re

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_migrate import Migrate
from email_validator import validate_email, EmailNotValidError
from sqlalchemy.exc import IntegrityError

from config import Config
from models import db, Destination, ContactMessage, Booking, NewsletterSubscriber


EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
PHONE_RE = re.compile(r"^[0-9+\-\s()]{7,20}$")


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    Migrate(app, db)

    CORS(
        app,
        resources={r"/api/*": {"origins": [Config.FRONTEND_ORIGIN, "http://localhost:4200"]}},
        supports_credentials=False,
    )

    register_routes(app)

    with app.app_context():
        db.create_all()

    return app


def register_routes(app: Flask):

    @app.get("/api/health")
    def health():
        return jsonify({"status": "ok", "service": Config.COMPANY_NAME, "time": datetime.utcnow().isoformat()})

    @app.get("/api/company")
    def company():
        return jsonify({
            "name": Config.COMPANY_NAME,
            "tagline": Config.COMPANY_TAGLINE,
            "ownerEmail": Config.OWNER_EMAIL,
        })

    # ---------- Destinations ----------
    @app.get("/api/destinations")
    def list_destinations():
        featured = request.args.get("featured")
        q = Destination.query
        if featured in ("1", "true", "yes"):
            q = q.filter(Destination.is_featured.is_(True))
        items = q.order_by(Destination.is_featured.desc(), Destination.id.asc()).all()
        return jsonify([d.to_dict() for d in items])

    @app.get("/api/destinations/<int:dest_id>")
    def get_destination(dest_id: int):
        d = Destination.query.get(dest_id)
        if not d:
            return jsonify({"error": "Destination not found"}), 404
        return jsonify(d.to_dict())

    # ---------- Contact ----------
    @app.post("/api/contact")
    def submit_contact():
        data = request.get_json(silent=True) or {}

        errors = {}
        name = (data.get("name") or "").strip()
        email = (data.get("email") or "").strip()
        message = (data.get("message") or "").strip()
        phone = (data.get("phone") or "").strip() or None
        subject = (data.get("subject") or "").strip() or None

        if len(name) < 2:
            errors["name"] = "Name must be at least 2 characters."
        try:
            validate_email(email, check_deliverability=False)
        except EmailNotValidError:
            errors["email"] = "Please provide a valid email address."
        if len(message) < 10:
            errors["message"] = "Message must be at least 10 characters."
        if phone and not PHONE_RE.match(phone):
            errors["phone"] = "Phone number looks invalid."

        if errors:
            return jsonify({"error": "Validation failed", "fields": errors}), 400

        msg = ContactMessage(
            name=name, email=email, phone=phone, subject=subject, message=message
        )
        db.session.add(msg)
        db.session.commit()

        return jsonify({
            "ok": True,
            "message": "Thank you! Your time-travel inquiry has been received.",
            "data": msg.to_dict(),
        }), 201

    @app.get("/api/contact")
    def list_contact_messages():
        items = ContactMessage.query.order_by(ContactMessage.created_at.desc()).limit(200).all()
        return jsonify([m.to_dict() for m in items])

    # ---------- Bookings ----------
    @app.post("/api/bookings")
    def create_booking():
        data = request.get_json(silent=True) or {}
        errors = {}

        try:
            destination_id = int(data.get("destinationId"))
        except (TypeError, ValueError):
            destination_id = None
            errors["destinationId"] = "Select a destination."

        full_name = (data.get("fullName") or "").strip()
        email = (data.get("email") or "").strip()
        phone = (data.get("phone") or "").strip()
        travelers_raw = data.get("travelers", 1)
        travel_date_raw = (data.get("travelDate") or "").strip()
        notes = (data.get("notes") or "").strip() or None

        if len(full_name) < 2:
            errors["fullName"] = "Full name is required."
        try:
            validate_email(email, check_deliverability=False)
        except EmailNotValidError:
            errors["email"] = "Valid email required."
        if not PHONE_RE.match(phone or ""):
            errors["phone"] = "Valid phone number required."

        try:
            travelers = int(travelers_raw)
            if travelers < 1 or travelers > 20:
                raise ValueError
        except (TypeError, ValueError):
            travelers = None
            errors["travelers"] = "Travelers must be between 1 and 20."

        try:
            travel_date = datetime.strptime(travel_date_raw, "%Y-%m-%d").date()
            if travel_date < datetime.utcnow().date():
                errors["travelDate"] = "Travel date must be in the future."
        except ValueError:
            travel_date = None
            errors["travelDate"] = "Travel date must be in YYYY-MM-DD format."

        if destination_id is not None and not Destination.query.get(destination_id):
            errors["destinationId"] = "Destination does not exist."

        if errors:
            return jsonify({"error": "Validation failed", "fields": errors}), 400

        booking = Booking(
            destination_id=destination_id,
            full_name=full_name,
            email=email,
            phone=phone,
            travelers=travelers,
            travel_date=travel_date,
            notes=notes,
        )
        db.session.add(booking)
        db.session.commit()

        return jsonify({
            "ok": True,
            "message": "Your time-travel booking is reserved! Our chrononauts will reach out within 24 hours.",
            "data": booking.to_dict(),
        }), 201

    @app.get("/api/bookings")
    def list_bookings():
        items = Booking.query.order_by(Booking.created_at.desc()).limit(200).all()
        return jsonify([b.to_dict() for b in items])

    # ---------- Newsletter ----------
    @app.post("/api/newsletter")
    def newsletter_subscribe():
        data = request.get_json(silent=True) or {}
        email = (data.get("email") or "").strip().lower()
        try:
            validate_email(email, check_deliverability=False)
        except EmailNotValidError:
            return jsonify({"error": "Please provide a valid email."}), 400

        try:
            sub = NewsletterSubscriber(email=email)
            db.session.add(sub)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return jsonify({"ok": True, "message": "You're already aboard the time train!"}), 200

        return jsonify({"ok": True, "message": "Welcome aboard, time traveller!"}), 201

    # ---------- Errors ----------
    @app.errorhandler(404)
    def not_found(_e):
        return jsonify({"error": "Not found"}), 404

    @app.errorhandler(500)
    def server_error(_e):
        return jsonify({"error": "Internal server error"}), 500


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
