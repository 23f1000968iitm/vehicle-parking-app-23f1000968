from datetime import datetime, timedelta
from .extensions import make_celery
from .models import Reservation, User
import csv
import os

# ⚠️ DO NOT import create_app here at top-level
# This will be imported only when needed


def _export_path(user_id: int) -> str:
    export_dir = os.path.join(os.path.dirname(__file__), "../frontend/exports")
    os.makedirs(export_dir, exist_ok=True)
    return os.path.join(export_dir, f"user_{user_id}_reservations.csv")


# ✅ Initialize Celery *without creating app yet*
celery = make_celery(lambda: None)


@celery.task
def export_reservations_csv_task(user_id: int):
    """Export a user's reservation history to CSV."""
    from .app import create_app  # 🔁 Imported lazily to avoid circular import

    app = create_app()
    with app.app_context():
        reservations = Reservation.query.filter_by(user_id=user_id).order_by(
            Reservation.parking_timestamp.asc()
        ).all()

        path = _export_path(user_id)
        with open(path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["reservation_id", "spot_id", "lot", "start", "end", "cost"])
            for r in reservations:
                writer.writerow([
                    r.id,
                    r.spot_id,
                    r.spot.lot.prime_location_name if r.spot and r.spot.lot else "",
                    r.parking_timestamp.isoformat(),
                    r.leaving_timestamp.isoformat() if r.leaving_timestamp else "",
                    r.parking_cost,
                ])

        return {"status": "done", "path": path}


@celery.task
def daily_reminder_task():
    """Notify users who haven’t booked in 14 days."""
    from .app import create_app

    app = create_app()
    with app.app_context():
        since = datetime.utcnow() - timedelta(days=14)
        users = User.query.filter(User.role == "user").all()
        quiet_users = []
        for u in users:
            has_recent = (
                Reservation.query.filter(
                    Reservation.user_id == u.id,
                    Reservation.parking_timestamp >= since,
                ).count()
                > 0
            )
            if not has_recent:
                quiet_users.append(u.email)
        print("[Daily Reminder] Consider booking a parking spot:", quiet_users)
        return {"reminded": quiet_users}


@celery.task
def monthly_report_task():
    """Generate a simple monthly usage report per user."""
    from .app import create_app

    app = create_app()
    with app.app_context():
        now = datetime.utcnow()
        first = datetime(now.year, now.month, 1)
        prev_month_end = first - timedelta(days=1)
        prev_first = datetime(prev_month_end.year, prev_month_end.month, 1)

        users = User.query.filter(User.role == "user").all()
        reports = {}
        for u in users:
            qs = Reservation.query.filter(
                Reservation.user_id == u.id,
                Reservation.parking_timestamp >= prev_first,
                Reservation.parking_timestamp <= prev_month_end,
            )
            total = qs.count()
            spent = sum(r.parking_cost or 0 for r in qs)
            by_lot = {}
            for r in qs:
                if r.spot and r.spot.lot:
                    name = r.spot.lot.prime_location_name
                    by_lot[name] = by_lot.get(name, 0) + 1
            reports[u.email] = {"bookings": total, "spent": spent, "by_lot": by_lot}

        print("[Monthly Report]", reports)
        return reports