"""
Utility helpers to populate the SQLite demo database with realistic data.
Used by seed_db.py and at application startup to guarantee a consistent dataset.
"""
from datetime import datetime, timedelta
import random

from models import db, User, ParkingLot, ParkingSpot, Reservation

LOT_BLUEPRINTS = [
    {
        "prime_location_name": "Downtown Mall Parking",
        "address": "123 Main Street, Downtown",
        "pin_code": "400001",
        "price_per_hour": 25.0,
        "number_of_spots": 36,
    },
    {
        "prime_location_name": "Seaside Business Hub",
        "address": "48 Marina Road, Harbour District",
        "pin_code": "400002",
        "price_per_hour": 30.0,
        "number_of_spots": 28,
    },
    {
        "prime_location_name": "Tech Park Annex",
        "address": "901 Innovation Drive, IT Corridor",
        "pin_code": "400003",
        "price_per_hour": 35.0,
        "number_of_spots": 32,
    },
    {
        "prime_location_name": "Airport Express Parking",
        "address": "Terminal 2, Departures Lane",
        "pin_code": "400004",
        "price_per_hour": 45.0,
        "number_of_spots": 40,
    },
    {
        "prime_location_name": "Cultural Center Parking",
        "address": "77 Heritage Square",
        "pin_code": "400005",
        "price_per_hour": 18.0,
        "number_of_spots": 30,
    },
]

USER_BLUEPRINTS = [
    {"username": "user1", "email": "user1@example.com", "password": "user1pass"},
    {"username": "user2", "email": "user2@example.com", "password": "user2pass"},
    {"username": "user3", "email": "user3@example.com", "password": "user3pass"},
    {"username": "user4", "email": "user4@example.com", "password": "user4pass"},
    {"username": "user5", "email": "user5@example.com", "password": "user5pass"},
]


def _ensure_lots():
    """Create lots and their spots if they are missing or under-provisioned."""
    created_lots = []
    for blueprint in LOT_BLUEPRINTS:
        lot = ParkingLot.query.filter_by(
            prime_location_name=blueprint["prime_location_name"]
        ).first()

        if not lot:
            lot = ParkingLot(**blueprint)
            db.session.add(lot)
            db.session.flush()

        # Guarantee that the number of spots matches blueprint
        existing_spot_count = ParkingSpot.query.filter_by(lot_id=lot.id).count()
        if existing_spot_count < blueprint["number_of_spots"]:
            for index in range(existing_spot_count + 1, blueprint["number_of_spots"] + 1):
                spot = ParkingSpot(
                    lot_id=lot.id,
                    spot_number=f"{chr(64 + ((index - 1) // 10) + 1)}{((index - 1) % 10) + 1}",
                    status="A",
                )
                db.session.add(spot)

        created_lots.append(lot)

    db.session.commit()
    return created_lots


def _ensure_users():
    """Create demo users if not already present."""
    created_users = []
    for blueprint in USER_BLUEPRINTS:
        user = User.query.filter_by(username=blueprint["username"]).first()
        if not user:
            user = User(
                username=blueprint["username"],
                email=blueprint["email"],
                phone_number="9876543210",
                address="Demo User Residency",
                pincode="400000",
                role="user",
            )
            user.set_password(blueprint["password"])
            db.session.add(user)
            db.session.flush()
        created_users.append(user)

    db.session.commit()
    return created_users


def _create_reservations(users, lots):
    """Populate reservations so dashboards and reports look realistic."""
    if Reservation.query.count() >= 25:
        return

    all_spots = ParkingSpot.query.all()
    random.seed(42)

    for user in users:
        # Completed reservations
        for _ in range(2):
            spot = random.choice(all_spots)
            lot = next((l for l in lots if l.id == spot.lot_id), None)
            if not lot:
                continue
            start_time = datetime.utcnow() - timedelta(days=random.randint(2, 14), hours=random.randint(1, 6))
            end_time = start_time + timedelta(hours=random.randint(1, 5))
            duration_hours = max((end_time - start_time).total_seconds() / 3600, 1)
            cost = round(duration_hours * lot.price_per_hour, 2)
            reservation = Reservation(
                user_id=user.id,
                spot_id=spot.id,
                parking_timestamp=start_time,
                leaving_timestamp=end_time,
                parking_cost=cost,
            )
            db.session.add(reservation)

        # Active reservation for first two users
        if user.username in ("user1", "user2"):
            available_spot = next((s for s in all_spots if s.status == "A"), None)
            if available_spot:
                available_spot.status = "O"
                active_start = datetime.utcnow() - timedelta(hours=random.randint(1, 3))
                active_reservation = Reservation(
                    user_id=user.id,
                    spot_id=available_spot.id,
                    parking_timestamp=active_start,
                    leaving_timestamp=None,
                    parking_cost=0.0,
                )
                db.session.add(active_reservation)

    db.session.commit()


def seed_demo_data(force_reset=False):
    """
    Populate the database with repeatable demo content.
    force_reset=True clears existing non-admin data before seeding.
    """
    if force_reset:
        Reservation.query.delete()
        ParkingSpot.query.delete()
        ParkingLot.query.delete()
        User.query.filter(User.role != "admin").delete()
        db.session.commit()

    lots = _ensure_lots()
    users = _ensure_users()
    _create_reservations(users, lots)

    print("✅ Demo dataset ensured. Lots: {}, Users: {}, Reservations: {}".format(
        ParkingLot.query.count(),
        User.query.filter_by(role="user").count(),
        Reservation.query.count(),
    ))

