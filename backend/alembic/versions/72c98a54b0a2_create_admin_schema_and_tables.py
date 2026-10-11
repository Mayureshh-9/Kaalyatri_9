"""create_admin_schema_and_tables

Revision ID: 72c98a54b0a2
Revises: 
Create Date: 2026-07-06 13:40:50.256503

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '72c98a54b0a2'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# SQL definitions for stored procedures
FUNCTIONS_SQL = [
    # 1. users
    """
    CREATE OR REPLACE FUNCTION admin.insert_update_user(
        p_email VARCHAR,
        p_full_name VARCHAR,
        p_phone VARCHAR,
        p_password_hash VARCHAR,
        p_is_admin BOOLEAN,
        p_created_by VARCHAR,
        p_id INTEGER
    ) RETURNS INTEGER AS $$
    DECLARE
        v_id INTEGER;
    BEGIN
        IF p_id IS NULL OR p_id = 0 THEN
            INSERT INTO admin.users (email, full_name, phone, password_hash, is_admin, created_date, created_by, updated_date, updated_by)
            VALUES (p_email, p_full_name, p_phone, p_password_hash, COALESCE(p_is_admin, FALSE), NOW(), p_created_by, NOW(), p_created_by)
            RETURNING id INTO v_id;
        ELSE
            UPDATE admin.users
            SET email = p_email,
                full_name = p_full_name,
                phone = p_phone,
                password_hash = p_password_hash,
                is_admin = COALESCE(p_is_admin, is_admin),
                updated_date = NOW(),
                updated_by = p_created_by
            WHERE id = p_id
            RETURNING id INTO v_id;
        END IF;
        RETURN v_id;
    END;
    $$ LANGUAGE plpgsql;
    """,
    """
    CREATE OR REPLACE FUNCTION admin.get_all_users(
        p_limit INTEGER,
        p_offset INTEGER,
        p_search VARCHAR
    ) RETURNS TABLE(
        id INTEGER,
        email VARCHAR,
        full_name VARCHAR,
        phone VARCHAR,
        password_hash VARCHAR,
        is_admin BOOLEAN,
        created_date TIMESTAMP,
        created_by VARCHAR,
        updated_date TIMESTAMP,
        updated_by VARCHAR,
        user_id INTEGER
    ) AS $$
    BEGIN
        RETURN QUERY
        SELECT u.id, u.email, u.full_name, u.phone, u.password_hash, u.is_admin, u.created_date, u.created_by, u.updated_date, u.updated_by, u.user_id
        FROM admin.users u
        WHERE (p_search IS NULL OR u.email ILIKE '%' || p_search || '%' OR u.full_name ILIKE '%' || p_search || '%')
        LIMIT p_limit OFFSET p_offset;
    END;
    $$ LANGUAGE plpgsql;
    """,
    """
    CREATE OR REPLACE FUNCTION admin.get_user_by_id(p_user_id INTEGER)
    RETURNS TABLE(
        id INTEGER,
        email VARCHAR,
        full_name VARCHAR,
        phone VARCHAR,
        password_hash VARCHAR,
        is_admin BOOLEAN,
        created_date TIMESTAMP,
        created_by VARCHAR,
        updated_date TIMESTAMP,
        updated_by VARCHAR,
        user_id INTEGER
    ) AS $$
    BEGIN
        RETURN QUERY
        SELECT u.id, u.email, u.full_name, u.phone, u.password_hash, u.is_admin, u.created_date, u.created_by, u.updated_date, u.updated_by, u.user_id
        FROM admin.users u
        WHERE u.id = p_user_id;
    END;
    $$ LANGUAGE plpgsql;
    """,
    """
    CREATE OR REPLACE FUNCTION admin.delete_user(p_id INTEGER, p_deleted_by INTEGER)
    RETURNS VARCHAR AS $$
    BEGIN
        DELETE FROM admin.users WHERE id = p_id;
        RETURN 'User deleted successfully';
    END;
    $$ LANGUAGE plpgsql;
    """,

    # 2. destinations
    """
    CREATE OR REPLACE FUNCTION admin.insert_update_destination(
        p_name VARCHAR,
        p_era VARCHAR,
        p_year_label VARCHAR,
        p_short_description VARCHAR,
        p_description TEXT,
        p_price_inr NUMERIC,
        p_duration_days INTEGER,
        p_difficulty VARCHAR,
        p_image_emoji VARCHAR,
        p_accent_color VARCHAR,
        p_highlights TEXT,
        p_is_featured BOOLEAN,
        p_created_by VARCHAR,
        p_id INTEGER
    ) RETURNS INTEGER AS $$
    DECLARE
        v_id INTEGER;
    BEGIN
        IF p_id IS NULL OR p_id = 0 THEN
            INSERT INTO admin.destinations (name, era, year_label, short_description, description, price_inr, duration_days, difficulty, image_emoji, accent_color, highlights, is_featured, created_date, created_by, updated_date, updated_by)
            VALUES (p_name, p_era, p_year_label, p_short_description, p_description, p_price_inr, COALESCE(p_duration_days, 7), p_difficulty, p_image_emoji, p_accent_color, p_highlights, COALESCE(p_is_featured, FALSE), NOW(), p_created_by, NOW(), p_created_by)
            RETURNING id INTO v_id;
        ELSE
            UPDATE admin.destinations
            SET name = p_name,
                era = p_era,
                year_label = p_year_label,
                short_description = p_short_description,
                description = p_description,
                price_inr = p_price_inr,
                duration_days = COALESCE(p_duration_days, duration_days),
                difficulty = p_difficulty,
                image_emoji = p_image_emoji,
                accent_color = p_accent_color,
                highlights = p_highlights,
                is_featured = COALESCE(p_is_featured, is_featured),
                updated_date = NOW(),
                updated_by = p_created_by
            WHERE id = p_id
            RETURNING id INTO v_id;
        END IF;
        RETURN v_id;
    END;
    $$ LANGUAGE plpgsql;
    """,
    """
    CREATE OR REPLACE FUNCTION admin.get_all_destinations(
        p_limit INTEGER,
        p_offset INTEGER,
        p_search VARCHAR,
        p_is_featured BOOLEAN
    ) RETURNS TABLE(
        id INTEGER,
        name VARCHAR,
        era VARCHAR,
        year_label VARCHAR,
        short_description VARCHAR,
        description TEXT,
        price_inr NUMERIC,
        duration_days INTEGER,
        difficulty VARCHAR,
        image_emoji VARCHAR,
        accent_color VARCHAR,
        highlights TEXT,
        is_featured BOOLEAN,
        created_date TIMESTAMP,
        created_by VARCHAR,
        updated_date TIMESTAMP,
        updated_by VARCHAR,
        user_id INTEGER
    ) AS $$
    BEGIN
        RETURN QUERY
        SELECT d.id, d.name, d.era, d.year_label, d.short_description, d.description, d.price_inr, d.duration_days, d.difficulty, d.image_emoji, d.accent_color, d.highlights, d.is_featured, d.created_date, d.created_by, d.updated_date, d.updated_by, d.user_id
        FROM admin.destinations d
        WHERE (p_search IS NULL OR d.name ILIKE '%' || p_search || '%' OR d.description ILIKE '%' || p_search || '%' OR d.era ILIKE '%' || p_search || '%')
          AND (p_is_featured IS NULL OR d.is_featured = p_is_featured)
        LIMIT p_limit OFFSET p_offset;
    END;
    $$ LANGUAGE plpgsql;
    """,
    """
    CREATE OR REPLACE FUNCTION admin.get_destination_by_id(p_destination_id INTEGER)
    RETURNS TABLE(
        id INTEGER,
        name VARCHAR,
        era VARCHAR,
        year_label VARCHAR,
        short_description VARCHAR,
        description TEXT,
        price_inr NUMERIC,
        duration_days INTEGER,
        difficulty VARCHAR,
        image_emoji VARCHAR,
        accent_color VARCHAR,
        highlights TEXT,
        is_featured BOOLEAN,
        created_date TIMESTAMP,
        created_by VARCHAR,
        updated_date TIMESTAMP,
        updated_by VARCHAR,
        user_id INTEGER
    ) AS $$
    BEGIN
        RETURN QUERY
        SELECT d.id, d.name, d.era, d.year_label, d.short_description, d.description, d.price_inr, d.duration_days, d.difficulty, d.image_emoji, d.accent_color, d.highlights, d.is_featured, d.created_date, d.created_by, d.updated_date, d.updated_by, d.user_id
        FROM admin.destinations d
        WHERE d.id = p_destination_id;
    END;
    $$ LANGUAGE plpgsql;
    """,
    """
    CREATE OR REPLACE FUNCTION admin.delete_destination(p_id INTEGER, p_deleted_by INTEGER)
    RETURNS VARCHAR AS $$
    BEGIN
        DELETE FROM admin.destinations WHERE id = p_id;
        RETURN 'Destination deleted successfully';
    END;
    $$ LANGUAGE plpgsql;
    """,

    # 3. bookings
    """
    CREATE OR REPLACE FUNCTION admin.insert_update_booking(
        p_destination_id INTEGER,
        p_full_name VARCHAR,
        p_email VARCHAR,
        p_phone VARCHAR,
        p_travelers INTEGER,
        p_travel_date DATE,
        p_notes TEXT,
        p_status VARCHAR,
        p_created_by VARCHAR,
        p_id INTEGER
    ) RETURNS INTEGER AS $$
    DECLARE
        v_id INTEGER;
    BEGIN
        IF p_id IS NULL OR p_id = 0 THEN
            INSERT INTO admin.bookings (destination_id, full_name, email, phone, travelers, travel_date, notes, status, created_date, created_by, updated_date, updated_by)
            VALUES (p_destination_id, p_full_name, p_email, p_phone, COALESCE(p_travelers, 1), p_travel_date, p_notes, COALESCE(p_status, 'pending'), NOW(), p_created_by, NOW(), p_created_by)
            RETURNING id INTO v_id;
        ELSE
            UPDATE admin.bookings
            SET destination_id = p_destination_id,
                full_name = p_full_name,
                email = p_email,
                phone = p_phone,
                travelers = COALESCE(p_travelers, travelers),
                travel_date = p_travel_date,
                notes = p_notes,
                status = COALESCE(p_status, status),
                updated_date = NOW(),
                updated_by = p_created_by
            WHERE id = p_id
            RETURNING id INTO v_id;
        END IF;
        RETURN v_id;
    END;
    $$ LANGUAGE plpgsql;
    """,
    """
    CREATE OR REPLACE FUNCTION admin.get_all_bookings(
        p_limit INTEGER,
        p_offset INTEGER,
        p_search VARCHAR,
        p_status VARCHAR
    ) RETURNS TABLE(
        id INTEGER,
        destination_id INTEGER,
        full_name VARCHAR,
        email VARCHAR,
        phone VARCHAR,
        travelers INTEGER,
        travel_date DATE,
        notes TEXT,
        status VARCHAR,
        created_date TIMESTAMP,
        created_by VARCHAR,
        updated_date TIMESTAMP,
        updated_by VARCHAR,
        user_id INTEGER
    ) AS $$
    BEGIN
        RETURN QUERY
        SELECT b.id, b.destination_id, b.full_name, b.email, b.phone, b.travelers, b.travel_date, b.notes, b.status, b.created_date, b.created_by, b.updated_date, b.updated_by, b.user_id
        FROM admin.bookings b
        WHERE (p_search IS NULL OR b.full_name ILIKE '%' || p_search || '%' OR b.email ILIKE '%' || p_search || '%')
          AND (p_status IS NULL OR b.status = p_status)
        LIMIT p_limit OFFSET p_offset;
    END;
    $$ LANGUAGE plpgsql;
    """,
    """
    CREATE OR REPLACE FUNCTION admin.get_booking_by_id(p_booking_id INTEGER)
    RETURNS TABLE(
        id INTEGER,
        destination_id INTEGER,
        full_name VARCHAR,
        email VARCHAR,
        phone VARCHAR,
        travelers INTEGER,
        travel_date DATE,
        notes TEXT,
        status VARCHAR,
        created_date TIMESTAMP,
        created_by VARCHAR,
        updated_date TIMESTAMP,
        updated_by VARCHAR,
        user_id INTEGER
    ) AS $$
    BEGIN
        RETURN QUERY
        SELECT b.id, b.destination_id, b.full_name, b.email, b.phone, b.travelers, b.travel_date, b.notes, b.status, b.created_date, b.created_by, b.updated_date, b.updated_by, b.user_id
        FROM admin.bookings b
        WHERE b.id = p_booking_id;
    END;
    $$ LANGUAGE plpgsql;
    """,
    """
    CREATE OR REPLACE FUNCTION admin.delete_booking(p_id INTEGER, p_deleted_by INTEGER)
    RETURNS VARCHAR AS $$
    BEGIN
        DELETE FROM admin.bookings WHERE id = p_id;
        RETURN 'Booking deleted successfully';
    END;
    $$ LANGUAGE plpgsql;
    """,

    # 4. contact_messages
    """
    CREATE OR REPLACE FUNCTION admin.insert_update_contact_message(
        p_name VARCHAR,
        p_email VARCHAR,
        p_phone VARCHAR,
        p_subject VARCHAR,
        p_message TEXT,
        p_is_read BOOLEAN,
        p_created_by VARCHAR,
        p_id INTEGER
    ) RETURNS INTEGER AS $$
    DECLARE
        v_id INTEGER;
    BEGIN
        IF p_id IS NULL OR p_id = 0 THEN
            INSERT INTO admin.contact_messages (name, email, phone, subject, message, is_read, created_date, created_by, updated_date, updated_by)
            VALUES (p_name, p_email, p_phone, p_subject, p_message, COALESCE(p_is_read, FALSE), NOW(), p_created_by, NOW(), p_created_by)
            RETURNING id INTO v_id;
        ELSE
            UPDATE admin.contact_messages
            SET name = p_name,
                email = p_email,
                phone = p_phone,
                subject = p_subject,
                message = p_message,
                is_read = COALESCE(p_is_read, is_read),
                updated_date = NOW(),
                updated_by = p_created_by
            WHERE id = p_id
            RETURNING id INTO v_id;
        END IF;
        RETURN v_id;
    END;
    $$ LANGUAGE plpgsql;
    """,
    """
    CREATE OR REPLACE FUNCTION admin.get_all_contact_messages(
        p_limit INTEGER,
        p_offset INTEGER,
        p_search VARCHAR,
        p_is_read BOOLEAN
    ) RETURNS TABLE(
        id INTEGER,
        name VARCHAR,
        email VARCHAR,
        phone VARCHAR,
        subject VARCHAR,
        message TEXT,
        is_read BOOLEAN,
        created_date TIMESTAMP,
        created_by VARCHAR,
        updated_date TIMESTAMP,
        updated_by VARCHAR,
        user_id INTEGER
    ) AS $$
    BEGIN
        RETURN QUERY
        SELECT c.id, c.name, c.email, c.phone, c.subject, c.message, c.is_read, c.created_date, c.created_by, c.updated_date, c.updated_by, c.user_id
        FROM admin.contact_messages c
        WHERE (p_search IS NULL OR c.name ILIKE '%' || p_search || '%' OR c.email ILIKE '%' || p_search || '%' OR c.subject ILIKE '%' || p_search || '%')
          AND (p_is_read IS NULL OR c.is_read = p_is_read)
        LIMIT p_limit OFFSET p_offset;
    END;
    $$ LANGUAGE plpgsql;
    """,
    """
    CREATE OR REPLACE FUNCTION admin.get_contact_message_by_id(p_contact_message_id INTEGER)
    RETURNS TABLE(
        id INTEGER,
        name VARCHAR,
        email VARCHAR,
        phone VARCHAR,
        subject VARCHAR,
        message TEXT,
        is_read BOOLEAN,
        created_date TIMESTAMP,
        created_by VARCHAR,
        updated_date TIMESTAMP,
        updated_by VARCHAR,
        user_id INTEGER
    ) AS $$
    BEGIN
        RETURN QUERY
        SELECT c.id, c.name, c.email, c.phone, c.subject, c.message, c.is_read, c.created_date, c.created_by, c.updated_date, c.updated_by, c.user_id
        FROM admin.contact_messages c
        WHERE c.id = p_contact_message_id;
    END;
    $$ LANGUAGE plpgsql;
    """,
    """
    CREATE OR REPLACE FUNCTION admin.delete_contact_message(p_id INTEGER, p_deleted_by INTEGER)
    RETURNS VARCHAR AS $$
    BEGIN
        DELETE FROM admin.contact_messages WHERE id = p_id;
        RETURN 'Contact message deleted successfully';
    END;
    $$ LANGUAGE plpgsql;
    """,

    # 5. newsletter_subscribers
    """
    CREATE OR REPLACE FUNCTION admin.insert_update_newsletter_subscriber(
        p_email VARCHAR,
        p_created_by VARCHAR,
        p_id INTEGER
    ) RETURNS INTEGER AS $$
    DECLARE
        v_id INTEGER;
    BEGIN
        IF p_id IS NULL OR p_id = 0 THEN
            INSERT INTO admin.newsletter_subscribers (email, created_date, created_by, updated_date, updated_by)
            VALUES (p_email, NOW(), p_created_by, NOW(), p_created_by)
            RETURNING id INTO v_id;
        ELSE
            UPDATE admin.newsletter_subscribers
            SET email = p_email,
                updated_date = NOW(),
                updated_by = p_created_by
            WHERE id = p_id
            RETURNING id INTO v_id;
        END IF;
        RETURN v_id;
    END;
    $$ LANGUAGE plpgsql;
    """,
    """
    CREATE OR REPLACE FUNCTION admin.get_all_newsletter_subscribers(
        p_limit INTEGER,
        p_offset INTEGER,
        p_search VARCHAR
    ) RETURNS TABLE(
        id INTEGER,
        email VARCHAR,
        created_date TIMESTAMP,
        created_by VARCHAR,
        updated_date TIMESTAMP,
        updated_by VARCHAR,
        user_id INTEGER
    ) AS $$
    BEGIN
        RETURN QUERY
        SELECT n.id, n.email, n.created_date, n.created_by, n.updated_date, n.updated_by, n.user_id
        FROM admin.newsletter_subscribers n
        WHERE (p_search IS NULL OR n.email ILIKE '%' || p_search || '%')
        LIMIT p_limit OFFSET p_offset;
    END;
    $$ LANGUAGE plpgsql;
    """,
    """
    CREATE OR REPLACE FUNCTION admin.get_newsletter_subscriber_by_id(p_subscriber_id INTEGER)
    RETURNS TABLE(
        id INTEGER,
        email VARCHAR,
        created_date TIMESTAMP,
        created_by VARCHAR,
        updated_date TIMESTAMP,
        updated_by VARCHAR,
        user_id INTEGER
    ) AS $$
    BEGIN
        RETURN QUERY
        SELECT n.id, n.email, n.created_date, n.created_by, n.updated_date, n.updated_by, n.user_id
        FROM admin.newsletter_subscribers n
        WHERE n.id = p_subscriber_id;
    END;
    $$ LANGUAGE plpgsql;
    """,
    """
    CREATE OR REPLACE FUNCTION admin.delete_newsletter_subscriber(p_id INTEGER, p_deleted_by INTEGER)
    RETURNS VARCHAR AS $$
    BEGIN
        DELETE FROM admin.newsletter_subscribers WHERE id = p_id;
        RETURN 'Subscriber deleted successfully';
    END;
    $$ LANGUAGE plpgsql;
    """,

    # 6. reviews
    """
    CREATE OR REPLACE FUNCTION admin.insert_update_review(
        p_destination_id INTEGER,
        p_rating INTEGER,
        p_comment TEXT,
        p_created_by VARCHAR,
        p_id INTEGER
    ) RETURNS INTEGER AS $$
    DECLARE
        v_id INTEGER;
    BEGIN
        IF p_id IS NULL OR p_id = 0 THEN
            INSERT INTO admin.reviews (destination_id, rating, comment, created_date, created_by, updated_date, updated_by)
            VALUES (p_destination_id, p_rating, p_comment, NOW(), p_created_by, NOW(), p_created_by)
            RETURNING id INTO v_id;
        ELSE
            UPDATE admin.reviews
            SET destination_id = p_destination_id,
                rating = p_rating,
                comment = p_comment,
                updated_date = NOW(),
                updated_by = p_created_by
            WHERE id = p_id
            RETURNING id INTO v_id;
        END IF;
        RETURN v_id;
    END;
    $$ LANGUAGE plpgsql;
    """,
    """
    CREATE OR REPLACE FUNCTION admin.get_all_reviews(
        p_limit INTEGER,
        p_offset INTEGER,
        p_destination_id INTEGER
    ) RETURNS TABLE(
        id INTEGER,
        destination_id INTEGER,
        rating INTEGER,
        comment TEXT,
        created_date TIMESTAMP,
        created_by VARCHAR,
        updated_date TIMESTAMP,
        updated_by VARCHAR,
        user_id INTEGER
    ) AS $$
    BEGIN
        RETURN QUERY
        SELECT r.id, r.destination_id, r.rating, r.comment, r.created_date, r.created_by, r.updated_date, r.updated_by, r.user_id
        FROM admin.reviews r
        WHERE (p_destination_id IS NULL OR r.destination_id = p_destination_id)
        LIMIT p_limit OFFSET p_offset;
    END;
    $$ LANGUAGE plpgsql;
    """,
    """
    CREATE OR REPLACE FUNCTION admin.get_review_by_id(p_review_id INTEGER)
    RETURNS TABLE(
        id INTEGER,
        destination_id INTEGER,
        rating INTEGER,
        comment TEXT,
        created_date TIMESTAMP,
        created_by VARCHAR,
        updated_date TIMESTAMP,
        updated_by VARCHAR,
        user_id INTEGER
    ) AS $$
    BEGIN
        RETURN QUERY
        SELECT r.id, r.destination_id, r.rating, r.comment, r.created_date, r.created_by, r.updated_date, r.updated_by, r.user_id
        FROM admin.reviews r
        WHERE r.id = p_review_id;
    END;
    $$ LANGUAGE plpgsql;
    """,
    """
    CREATE OR REPLACE FUNCTION admin.delete_review(p_id INTEGER, p_deleted_by INTEGER)
    RETURNS VARCHAR AS $$
    BEGIN
        DELETE FROM admin.reviews WHERE id = p_id;
        RETURN 'Review deleted successfully';
    END;
    $$ LANGUAGE plpgsql;
    """,

    # 7. tour_itineraries
    """
    CREATE OR REPLACE FUNCTION admin.insert_update_tour_itinerary(
        p_destination_id INTEGER,
        p_day_number INTEGER,
        p_title VARCHAR,
        p_description TEXT,
        p_created_by VARCHAR,
        p_id INTEGER
    ) RETURNS INTEGER AS $$
    DECLARE
        v_id INTEGER;
    BEGIN
        IF p_id IS NULL OR p_id = 0 THEN
            INSERT INTO admin.tour_itineraries (destination_id, day_number, title, description, created_date, created_by, updated_date, updated_by)
            VALUES (p_destination_id, p_day_number, p_title, p_description, NOW(), p_created_by, NOW(), p_created_by)
            RETURNING id INTO v_id;
        ELSE
            UPDATE admin.tour_itineraries
            SET destination_id = p_destination_id,
                day_number = p_day_number,
                title = p_title,
                description = p_description,
                updated_date = NOW(),
                updated_by = p_created_by
            WHERE id = p_id
            RETURNING id INTO v_id;
        END IF;
        RETURN v_id;
    END;
    $$ LANGUAGE plpgsql;
    """,
    """
    CREATE OR REPLACE FUNCTION admin.get_all_tour_itineraries(
        p_limit INTEGER,
        p_offset INTEGER,
        p_destination_id INTEGER
    ) RETURNS TABLE(
        id INTEGER,
        destination_id INTEGER,
        day_number INTEGER,
        title VARCHAR,
        description TEXT,
        created_date TIMESTAMP,
        created_by VARCHAR,
        updated_date TIMESTAMP,
        updated_by VARCHAR,
        user_id INTEGER
    ) AS $$
    BEGIN
        RETURN QUERY
        SELECT t.id, t.destination_id, t.day_number, t.title, t.description, t.created_date, t.created_by, t.updated_date, t.updated_by, t.user_id
        FROM admin.tour_itineraries t
        WHERE (p_destination_id IS NULL OR t.destination_id = p_destination_id)
        ORDER BY t.day_number ASC
        LIMIT p_limit OFFSET p_offset;
    END;
    $$ LANGUAGE plpgsql;
    """,
    """
    CREATE OR REPLACE FUNCTION admin.get_tour_itinerary_by_id(p_itinerary_id INTEGER)
    RETURNS TABLE(
        id INTEGER,
        destination_id INTEGER,
        day_number INTEGER,
        title VARCHAR,
        description TEXT,
        created_date TIMESTAMP,
        created_by VARCHAR,
        updated_date TIMESTAMP,
        updated_by VARCHAR,
        user_id INTEGER
    ) AS $$
    BEGIN
        RETURN QUERY
        SELECT t.id, t.destination_id, t.day_number, t.title, t.description, t.created_date, t.created_by, t.updated_date, t.updated_by, t.user_id
        FROM admin.tour_itineraries t
        WHERE t.id = p_itinerary_id;
    END;
    $$ LANGUAGE plpgsql;
    """,
    """
    CREATE OR REPLACE FUNCTION admin.delete_tour_itinerary(p_id INTEGER, p_deleted_by INTEGER)
    RETURNS VARCHAR AS $$
    BEGIN
        DELETE FROM admin.tour_itineraries WHERE id = p_id;
        RETURN 'Itinerary deleted successfully';
    END;
    $$ LANGUAGE plpgsql;
    """,

    # 8. payments
    """
    CREATE OR REPLACE FUNCTION admin.insert_update_payment(
        p_booking_id INTEGER,
        p_amount NUMERIC,
        p_status VARCHAR,
        p_transaction_id VARCHAR,
        p_created_by VARCHAR,
        p_id INTEGER
    ) RETURNS INTEGER AS $$
    DECLARE
        v_id INTEGER;
    BEGIN
        IF p_id IS NULL OR p_id = 0 THEN
            INSERT INTO admin.payments (booking_id, amount, status, transaction_id, created_date, created_by, updated_date, updated_by)
            VALUES (p_booking_id, p_amount, COALESCE(p_status, 'Pending'), p_transaction_id, NOW(), p_created_by, NOW(), p_created_by)
            RETURNING id INTO v_id;
        ELSE
            UPDATE admin.payments
            SET booking_id = p_booking_id,
                amount = p_amount,
                status = p_status,
                transaction_id = p_transaction_id,
                updated_date = NOW(),
                updated_by = p_created_by
            WHERE id = p_id
            RETURNING id INTO v_id;
        END IF;
        RETURN v_id;
    END;
    $$ LANGUAGE plpgsql;
    """,
    """
    CREATE OR REPLACE FUNCTION admin.get_all_payments(
        p_limit INTEGER,
        p_offset INTEGER,
        p_booking_id INTEGER
    ) RETURNS TABLE(
        id INTEGER,
        booking_id INTEGER,
        amount NUMERIC,
        status VARCHAR,
        transaction_id VARCHAR,
        created_date TIMESTAMP,
        created_by VARCHAR,
        updated_date TIMESTAMP,
        updated_by VARCHAR,
        user_id INTEGER
    ) AS $$
    BEGIN
        RETURN QUERY
        SELECT p.id, p.booking_id, p.amount, p.status, p.transaction_id, p.created_date, p.created_by, p.updated_date, p.updated_by, p.user_id
        FROM admin.payments p
        WHERE (p_booking_id IS NULL OR p.booking_id = p_booking_id)
        LIMIT p_limit OFFSET p_offset;
    END;
    $$ LANGUAGE plpgsql;
    """,
    """
    CREATE OR REPLACE FUNCTION admin.get_payment_by_id(p_payment_id INTEGER)
    RETURNS TABLE(
        id INTEGER,
        booking_id INTEGER,
        amount NUMERIC,
        status VARCHAR,
        transaction_id VARCHAR,
        created_date TIMESTAMP,
        created_by VARCHAR,
        updated_date TIMESTAMP,
        updated_by VARCHAR,
        user_id INTEGER
    ) AS $$
    BEGIN
        RETURN QUERY
        SELECT p.id, p.booking_id, p.amount, p.status, p.transaction_id, p.created_date, p.created_by, p.updated_date, p.updated_by, p.user_id
        FROM admin.payments p
        WHERE p.id = p_payment_id;
    END;
    $$ LANGUAGE plpgsql;
    """,
    """
    CREATE OR REPLACE FUNCTION admin.delete_payment(p_id INTEGER, p_deleted_by INTEGER)
    RETURNS VARCHAR AS $$
    BEGIN
        DELETE FROM admin.payments WHERE id = p_id;
        RETURN 'Payment deleted successfully';
    END;
    $$ LANGUAGE plpgsql;
    """
]


def upgrade() -> None:
    """Upgrade schema."""
    # Create the admin schema first!
    op.execute("CREATE SCHEMA IF NOT EXISTS admin")

    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('contact_messages',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=120), nullable=False),
    sa.Column('email', sa.String(length=150), nullable=False),
    sa.Column('phone', sa.String(length=30), nullable=True),
    sa.Column('subject', sa.String(length=200), nullable=True),
    sa.Column('message', sa.Text(), nullable=False),
    sa.Column('is_read', sa.Boolean(), nullable=True),
    sa.Column('created_date', sa.DateTime(), nullable=False),
    sa.Column('created_by', sa.String(), nullable=True),
    sa.Column('updated_date', sa.DateTime(), nullable=False),
    sa.Column('updated_by', sa.String(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    schema='admin'
    )
    op.create_table('destinations',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=150), nullable=False),
    sa.Column('era', sa.String(length=100), nullable=False),
    sa.Column('year_label', sa.String(length=50), nullable=False),
    sa.Column('short_description', sa.String(length=255), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('price_inr', sa.Numeric(precision=12, scale=2), nullable=False),
    sa.Column('duration_days', sa.Integer(), nullable=False),
    sa.Column('difficulty', sa.String(length=50), nullable=True),
    sa.Column('image_emoji', sa.String(length=20), nullable=True),
    sa.Column('accent_color', sa.String(length=20), nullable=True),
    sa.Column('highlights', sa.Text(), nullable=True),
    sa.Column('is_featured', sa.Boolean(), nullable=True),
    sa.Column('created_date', sa.DateTime(), nullable=False),
    sa.Column('created_by', sa.String(), nullable=True),
    sa.Column('updated_date', sa.DateTime(), nullable=False),
    sa.Column('updated_by', sa.String(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    schema='admin'
    )
    op.create_table('newsletter_subscribers',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('email', sa.String(length=150), nullable=False),
    sa.Column('created_date', sa.DateTime(), nullable=False),
    sa.Column('created_by', sa.String(), nullable=True),
    sa.Column('updated_date', sa.DateTime(), nullable=False),
    sa.Column('updated_by', sa.String(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    schema='admin'
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('email', sa.String(length=150), nullable=False),
    sa.Column('full_name', sa.String(length=120), nullable=False),
    sa.Column('phone', sa.String(length=30), nullable=True),
    sa.Column('password_hash', sa.String(length=255), nullable=False),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.Column('created_date', sa.DateTime(), nullable=False),
    sa.Column('created_by', sa.String(), nullable=True),
    sa.Column('updated_date', sa.DateTime(), nullable=False),
    sa.Column('updated_by', sa.String(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    schema='admin'
    )
    op.create_table('bookings',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('destination_id', sa.Integer(), nullable=False),
    sa.Column('full_name', sa.String(length=120), nullable=False),
    sa.Column('email', sa.String(length=150), nullable=False),
    sa.Column('phone', sa.String(length=30), nullable=False),
    sa.Column('travelers', sa.Integer(), nullable=False),
    sa.Column('travel_date', sa.Date(), nullable=False),
    sa.Column('notes', sa.Text(), nullable=True),
    sa.Column('status', sa.String(length=30), nullable=True),
    sa.Column('created_date', sa.DateTime(), nullable=False),
    sa.Column('created_by', sa.String(), nullable=True),
    sa.Column('updated_date', sa.DateTime(), nullable=False),
    sa.Column('updated_by', sa.String(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['destination_id'], ['admin.destinations.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='admin'
    )
    op.create_table('reviews',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('destination_id', sa.Integer(), nullable=False),
    sa.Column('rating', sa.Integer(), nullable=False),
    sa.Column('comment', sa.Text(), nullable=True),
    sa.Column('created_date', sa.DateTime(), nullable=False),
    sa.Column('created_by', sa.String(), nullable=True),
    sa.Column('updated_date', sa.DateTime(), nullable=False),
    sa.Column('updated_by', sa.String(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['destination_id'], ['admin.destinations.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='admin'
    )
    op.create_table('tour_itineraries',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('destination_id', sa.Integer(), nullable=False),
    sa.Column('day_number', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=200), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('created_date', sa.DateTime(), nullable=False),
    sa.Column('created_by', sa.String(), nullable=True),
    sa.Column('updated_date', sa.DateTime(), nullable=False),
    sa.Column('updated_by', sa.String(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['destination_id'], ['admin.destinations.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='admin'
    )
    op.create_table('payments',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('booking_id', sa.Integer(), nullable=False),
    sa.Column('amount', sa.Numeric(precision=12, scale=2), nullable=False),
    sa.Column('status', sa.String(length=50), nullable=True),
    sa.Column('transaction_id', sa.String(length=100), nullable=True),
    sa.Column('created_date', sa.DateTime(), nullable=False),
    sa.Column('created_by', sa.String(), nullable=True),
    sa.Column('updated_date', sa.DateTime(), nullable=False),
    sa.Column('updated_by', sa.String(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['booking_id'], ['admin.bookings.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('transaction_id'),
    schema='admin'
    )
    
    # Drop public schema tables if they exist
    # Use execute to run drop table CASCADE if they exist
    op.execute("DROP TABLE IF EXISTS reviews CASCADE")
    op.execute("DROP TABLE IF EXISTS payments CASCADE")
    op.execute("DROP TABLE IF EXISTS tour_itineraries CASCADE")
    op.execute("DROP TABLE IF EXISTS bookings CASCADE")
    op.execute("DROP TABLE IF EXISTS destinations CASCADE")
    op.execute("DROP TABLE IF EXISTS newsletter_subscribers CASCADE")
    op.execute("DROP TABLE IF EXISTS contact_messages CASCADE")
    op.execute("DROP TABLE IF EXISTS users CASCADE")

    # Create stored procedures
    for sql in FUNCTIONS_SQL:
        op.execute(sql)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # Drop functions in admin schema
    op.execute("DROP FUNCTION IF EXISTS admin.delete_payment(INTEGER, INTEGER)")
    op.execute("DROP FUNCTION IF EXISTS admin.get_payment_by_id(INTEGER)")
    op.execute("DROP FUNCTION IF EXISTS admin.get_all_payments(INTEGER, INTEGER, INTEGER)")
    op.execute("DROP FUNCTION IF EXISTS admin.insert_update_payment(INTEGER, NUMERIC, VARCHAR, VARCHAR, VARCHAR, INTEGER)")

    op.execute("DROP FUNCTION IF EXISTS admin.delete_tour_itinerary(INTEGER, INTEGER)")
    op.execute("DROP FUNCTION IF EXISTS admin.get_tour_itinerary_by_id(INTEGER)")
    op.execute("DROP FUNCTION IF EXISTS admin.get_all_tour_itineraries(INTEGER, INTEGER, INTEGER)")
    op.execute("DROP FUNCTION IF EXISTS admin.insert_update_tour_itinerary(INTEGER, INTEGER, VARCHAR, TEXT, VARCHAR, INTEGER)")

    op.execute("DROP FUNCTION IF EXISTS admin.delete_review(INTEGER, INTEGER)")
    op.execute("DROP FUNCTION IF EXISTS admin.get_review_by_id(INTEGER)")
    op.execute("DROP FUNCTION IF EXISTS admin.get_all_reviews(INTEGER, INTEGER, INTEGER)")
    op.execute("DROP FUNCTION IF EXISTS admin.insert_update_review(INTEGER, INTEGER, TEXT, VARCHAR, INTEGER)")

    op.execute("DROP FUNCTION IF EXISTS admin.delete_newsletter_subscriber(INTEGER, INTEGER)")
    op.execute("DROP FUNCTION IF EXISTS admin.get_newsletter_subscriber_by_id(INTEGER)")
    op.execute("DROP FUNCTION IF EXISTS admin.get_all_newsletter_subscribers(INTEGER, INTEGER, VARCHAR)")
    op.execute("DROP FUNCTION IF EXISTS admin.insert_update_newsletter_subscriber(VARCHAR, VARCHAR, INTEGER)")

    op.execute("DROP FUNCTION IF EXISTS admin.delete_contact_message(INTEGER, INTEGER)")
    op.execute("DROP FUNCTION IF EXISTS admin.get_contact_message_by_id(INTEGER)")
    op.execute("DROP FUNCTION IF EXISTS admin.get_all_contact_messages(INTEGER, INTEGER, VARCHAR, BOOLEAN)")
    op.execute("DROP FUNCTION IF EXISTS admin.insert_update_contact_message(VARCHAR, VARCHAR, VARCHAR, VARCHAR, TEXT, BOOLEAN, VARCHAR, INTEGER)")

    op.execute("DROP FUNCTION IF EXISTS admin.delete_booking(INTEGER, INTEGER)")
    op.execute("DROP FUNCTION IF EXISTS admin.get_booking_by_id(INTEGER)")
    op.execute("DROP FUNCTION IF EXISTS admin.get_all_bookings(INTEGER, INTEGER, VARCHAR, VARCHAR)")
    op.execute("DROP FUNCTION IF EXISTS admin.insert_update_booking(INTEGER, VARCHAR, VARCHAR, VARCHAR, INTEGER, DATE, TEXT, VARCHAR, VARCHAR, INTEGER)")

    op.execute("DROP FUNCTION IF EXISTS admin.delete_destination(INTEGER, INTEGER)")
    op.execute("DROP FUNCTION IF EXISTS admin.get_destination_by_id(INTEGER)")
    op.execute("DROP FUNCTION IF EXISTS admin.get_all_destinations(INTEGER, INTEGER, VARCHAR, BOOLEAN)")
    op.execute("DROP FUNCTION IF EXISTS admin.insert_update_destination(VARCHAR, VARCHAR, VARCHAR, VARCHAR, TEXT, NUMERIC, INTEGER, VARCHAR, VARCHAR, VARCHAR, TEXT, BOOLEAN, VARCHAR, INTEGER)")

    op.execute("DROP FUNCTION IF EXISTS admin.delete_user(INTEGER, INTEGER)")
    op.execute("DROP FUNCTION IF EXISTS admin.get_user_by_id(INTEGER)")
    op.execute("DROP FUNCTION IF EXISTS admin.get_all_users(INTEGER, INTEGER, VARCHAR)")
    op.execute("DROP FUNCTION IF EXISTS admin.insert_update_user(VARCHAR, VARCHAR, VARCHAR, VARCHAR, BOOLEAN, VARCHAR, INTEGER)")

    op.drop_table('payments', schema='admin')
    op.drop_table('tour_itineraries', schema='admin')
    op.drop_table('reviews', schema='admin')
    op.drop_table('bookings', schema='admin')
    op.drop_table('users', schema='admin')
    op.drop_table('newsletter_subscribers', schema='admin')
    op.drop_table('destinations', schema='admin')
    op.drop_table('contact_messages', schema='admin')

    op.execute("DROP SCHEMA IF EXISTS admin CASCADE")
