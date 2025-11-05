from datetime import datetime
from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from ..extensions import db, cache
from ..models import ParkingLot, ParkingSpot, Reservation
from ..tasks import export_reservations_csv_task


user_bp = Blueprint("user", __name__)


@user_bp.get("/lots")
@login_required
@cache.cached(timeout=30, key_prefix="user_lots")
def list_lots():
    lots = ParkingLot.query.all()
    res = []
    for lot in lots:
        total = ParkingSpot.query.filter_by(lot_id=lot.id).count()
        available = ParkingSpot.query.filter_by(lot_id=lot.id, status="A").count()
        res.append({
            "id": lot.id,
            "name": lot.prime_location_name,
            "price": lot.price,
            "address": lot.address,
            "pin_code": lot.pin_code,
            "available": available,
            "total": total,
        })
    return jsonify(res)


@user_bp.post("/book")
@login_required
def book_first_available():
    data = request.get_json() or {}
    lot_id = int(data.get("lot_id"))
    spot = ParkingSpot.query.filter_by(lot_id=lot_id, status="A").first()
    if not spot:
        return jsonify({"error": "No spots available"}), 400
    spot.status = "O"
    res = Reservation(spot_id=spot.id, user_id=current_user.id, parking_timestamp=datetime.utcnow())
    db.session.add(res)
    db.session.commit()
    cache.delete("user_lots")
    return jsonify({"message": "Booked", "spot_id": spot.id, "reservation_id": res.id})


@user_bp.post("/release")
@login_required
def release_spot():
    data = request.get_json() or {}
    reservation_id = int(data.get("reservation_id"))
    res = Reservation.query.get_or_404(reservation_id)
    if res.user_id != current_user.id:
        return jsonify({"error": "Not your reservation"}), 403
    if res.leaving_timestamp:
        return jsonify({"message": "Already released"})
    res.leaving_timestamp = datetime.utcnow()
    # Simple cost: duration hours * lot price
    hours = max(1, int((res.leaving_timestamp - res.parking_timestamp).total_seconds() // 3600))
    lot_price = res.spot.lot.price
    res.parking_cost = hours * lot_price
    res.spot.status = "A"
    db.session.commit()
    cache.delete("user_lots")
    return jsonify({"message": "Released", "cost": res.parking_cost})


@user_bp.get("/history")
@login_required
def history():
    reservations = Reservation.query.filter_by(user_id=current_user.id).order_by(Reservation.parking_timestamp.desc()).all()
    result = []
    for r in reservations:
        result.append({
            "id": r.id,
            "spot_id": r.spot_id,
            "lot": r.spot.lot.prime_location_name,
            "from": r.parking_timestamp.isoformat(),
            "to": r.leaving_timestamp.isoformat() if r.leaving_timestamp else None,
            "cost": r.parking_cost,
        })
    return jsonify(result)


@user_bp.post("/export")
@login_required
def export_csv():
    task = export_reservations_csv_task.delay(current_user.id)
    return jsonify({"task_id": task.id, "message": "Export started"})



