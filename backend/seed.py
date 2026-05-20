"""Seed the database with KaalYatri time-travel destinations.

Run:  python seed.py
"""
from app import create_app
from models import db, Destination


DESTINATIONS = [
    {
        "name": "Ancient Egypt — Pyramid Era",
        "era": "Old Kingdom",
        "year_label": "2560 BCE",
        "short_description": "Witness the Great Pyramid rise stone by stone under Pharaoh Khufu.",
        "description": (
            "Travel to the banks of the Nile during the height of the Old Kingdom. "
            "Walk amongst the architects, watch quarrymen float limestone from Tura, "
            "and dine with priests of Ra. A safe-observer cloak keeps you invisible to locals."
        ),
        "price_inr": 184999,
        "duration_days": 8,
        "difficulty": "Easy",
        "image_emoji": "🏜️",
        "accent_color": "#f5b400",
        "highlights": "Great Pyramid construction|Nile sunset cruise|Hieroglyph workshop|Royal court banquet",
        "is_featured": True,
    },
    {
        "name": "Renaissance Florence",
        "era": "Italian Renaissance",
        "year_label": "1503 CE",
        "short_description": "Sip wine with Da Vinci as he sketches the Mona Lisa.",
        "description": (
            "Stroll the cobblestones of Medici-era Florence. Visit Leonardo's workshop, "
            "watch Michelangelo carve, and attend a private dinner at the Palazzo Vecchio. "
            "Includes period-correct attire and a translator earpiece."
        ),
        "price_inr": 219999,
        "duration_days": 6,
        "difficulty": "Easy",
        "image_emoji": "🎨",
        "accent_color": "#c9356b",
        "highlights": "Leonardo's workshop|Duomo rooftop tour|Medici banquet|Old-master sketching class",
        "is_featured": True,
    },
    {
        "name": "Mughal Agra — Taj Mahal Genesis",
        "era": "Mughal Empire",
        "year_label": "1648 CE",
        "short_description": "Walk through the Taj Mahal the year it was completed.",
        "description": (
            "Stand inside the freshly inlaid mausoleum before any tourist had laid eyes on it. "
            "Meet master artisans from Persia and Central Asia, taste imperial Mughlai cuisine, "
            "and ride an elephant through the royal Charbagh."
        ),
        "price_inr": 159999,
        "duration_days": 5,
        "difficulty": "Easy",
        "image_emoji": "🕌",
        "accent_color": "#26c2a8",
        "highlights": "Pristine Taj Mahal|Imperial elephant ride|Mughlai royal feast|Pietra dura inlay demo",
        "is_featured": True,
    },
    {
        "name": "Cretaceous Wilds",
        "era": "Late Cretaceous",
        "year_label": "66M BCE",
        "short_description": "Observe T. Rex and Triceratops from a hover-canopy.",
        "description": (
            "Float over a primeval North American floodplain in our shielded hover-canopy. "
            "See nesting hadrosaurs, stalking Tyrannosaurs, and the last great forests before the asteroid. "
            "Departures are scheduled to safely return before impact day."
        ),
        "price_inr": 389999,
        "duration_days": 4,
        "difficulty": "Adventurous",
        "image_emoji": "🦖",
        "accent_color": "#5cb85c",
        "highlights": "T. Rex tracking|Hover-canopy safari|Hadrosaur nesting site|Glowing nighttime forest",
        "is_featured": True,
    },
    {
        "name": "Victorian London",
        "era": "British Empire",
        "year_label": "1888 CE",
        "short_description": "Gas-lit streets, steam carriages, and a Sherlock-style mystery night.",
        "description": (
            "Stay at a private Mayfair townhouse, ride a steam-powered hansom, attend a music hall, "
            "and join an in-character detective evening solving a Whitechapel mystery. "
            "Period costumes and elocution coach included."
        ),
        "price_inr": 174999,
        "duration_days": 6,
        "difficulty": "Easy",
        "image_emoji": "🎩",
        "accent_color": "#9b6dff",
        "highlights": "Steam hansom rides|Music hall evening|Detective mystery night|Tea at Claridge's",
        "is_featured": False,
    },
    {
        "name": "Wild West Frontier",
        "era": "American Old West",
        "year_label": "1878 CE",
        "short_description": "Saloons, stagecoaches, and a cattle drive across Kansas plains.",
        "description": (
            "Trade your phone for a Stetson. Join a real cattle drive, learn to shoot a Colt at a safe range, "
            "and bunk in a frontier town. Optional poker night with hand-tinted period currency."
        ),
        "price_inr": 144999,
        "duration_days": 7,
        "difficulty": "Adventurous",
        "image_emoji": "🤠",
        "accent_color": "#e07b39",
        "highlights": "Cattle drive|Saloon poker night|Marksmanship lesson|Stagecoach ride",
        "is_featured": False,
    },
    {
        "name": "Mars Colony — New Olympus",
        "era": "Future",
        "year_label": "2174 CE",
        "short_description": "Walk the red sands of humanity's first million-citizen city.",
        "description": (
            "Touch down at New Olympus dome and ride a maglev to Olympus Mons base camp. "
            "Try Martian-grown cuisine, see the orbital ring under construction, "
            "and attend a zero-G concert above Valles Marineris."
        ),
        "price_inr": 499999,
        "duration_days": 9,
        "difficulty": "Intense",
        "image_emoji": "🪐",
        "accent_color": "#ff5470",
        "highlights": "Olympus Mons maglev|Zero-G concert|Martian cuisine|Orbital ring tour",
        "is_featured": True,
    },
    {
        "name": "Indus Valley — Mohenjo-daro",
        "era": "Bronze Age India",
        "year_label": "2400 BCE",
        "short_description": "Explore one of the world's first planned cities at its peak.",
        "description": (
            "Wander the grid streets and Great Bath of Mohenjo-daro alongside its citizens. "
            "Learn early Harappan script, visit a working seal-carver, and trade in the central market. "
            "An anthropologist guide travels with you throughout."
        ),
        "price_inr": 134999,
        "duration_days": 5,
        "difficulty": "Easy",
        "image_emoji": "🏺",
        "accent_color": "#36b6ff",
        "highlights": "Great Bath visit|Seal-carving workshop|Bronze Age market|Harappan script lesson",
        "is_featured": False,
    },
]


def seed():
    app = create_app()
    with app.app_context():
        if Destination.query.count() > 0:
            print(f"Destinations already seeded ({Destination.query.count()} rows). Skipping.")
            return
        for row in DESTINATIONS:
            db.session.add(Destination(**row))
        db.session.commit()
        print(f"Seeded {len(DESTINATIONS)} destinations.")


if __name__ == "__main__":
    seed()
