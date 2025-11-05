from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from ..extensions import db, cache
from ..models import ParkingLot, ParkingSpot, User, Reservation


admin_bp = Blueprint("admin", __name__)


def _require_admin():
    if not current_user.is_authenticated or current_user.role != "admin":
        return jsonify({"error": "Admin required"}), 403
    return None


@admin_bp.get("/users")
@login_required
def list_users():
    gate = _require_admin()
    if gate:
        return gate
    users = User.query.filter(User.role == "user").all()
    return jsonify([
        {"id": u.id, "name": u.name, "email": u.email} for u in users
    ])


@admin_bp.get("/lots")
@login_required
@cache.cached(timeout=30, key_prefix="admin_lots")
def get_lots():
    gate = _require_admin()
    if gate:
        return gate
    lots = ParkingLot.query.all()
    result = []
    for lot in lots:
        spots = ParkingSpot.query.filter_by(lot_id=lot.id).all()
        occupied = sum(1 for s in spots if s.status == "O")
        result.append({
            "id": lot.id,
            "prime_location_name": lot.prime_location_name,
            "address": lot.address,
            "pin_code": lot.pin_code,
            "price": lot.price,
            "number_of_spots": lot.number_of_spots,
            "occupied": occupied,
        })
    return jsonify(result)


@admin_bp.post("/lots")
@login_required
def create_lot():
    gate = _require_admin()
    if gate:
        return gate
    data = request.get_json() or {}
    lot = ParkingLot(
        prime_location_name=data.get("prime_location_name", "Unnamed"),
        address=data.get("address", ""),
        pin_code=str(data.get("pin_code", "")),
        price=int(data.get("price", 0)),
        number_of_spots=int(data.get("number_of_spots", 0)),
    )
    db.session.add(lot)
    db.session.flush()
    # Auto-create spots
    spots = [ParkingSpot(lot_id=lot.id, status="A") for _ in range(lot.number_of_spots)]
    db.session.add_all(spots)
    db.session.commit()
    cache.delete("admin_lots")
    return jsonify({"message": "Lot created", "id": lot.id})


@admin_bp.put("/lots/<int:lot_id>")
@login_required
def update_lot(lot_id):
    gate = _require_admin()
    if gate:
        return gate
    data = request.get_json() or {}
    lot = ParkingLot.query.get_or_404(lot_id)
    lot.prime_location_name = data.get("prime_location_name", lot.prime_location_name)
    lot.address = data.get("address", lot.address)
    lot.pin_code = str(data.get("pin_code", lot.pin_code))
    lot.price = int(data.get("price", lot.price))
    new_spots = int(data.get("number_of_spots", lot.number_of_spots))
    # Adjust spot count
    if new_spots != lot.number_of_spots:
        current_count = ParkingSpot.query.filter_by(lot_id=lot.id).count()
        if new_spots > current_count:
            add = new_spots - current_count
            db.session.add_all([ParkingSpot(lot_id=lot.id) for _ in range(add)])
        else:
            # Only delete available spots
            removable = ParkingSpot.query.filter_by(lot_id=lot.id, status="A").limit(current_count - new_spots).all()
            if len(removable) < (current_count - new_spots):
                return jsonify({"error": "Cannot reduce spots while occupied"}), 400
            for s in removable:
                db.session.delete(s)
        lot.number_of_spots = new_spots
    db.session.commit()
    cache.delete("admin_lots")
    return jsonify({"message": "Updated"})


@admin_bp.delete("/lots/<int:lot_id>")
@login_required
def delete_lot(lot_id):
    gate = _require_admin()
    if gate:
        return gate
    lot = ParkingLot.query.get_or_404(lot_id)
    occ = ParkingSpot.query.filter_by(lot_id=lot.id, status="O").count()
    if occ:
        return jsonify({"error": "Cannot delete lot with occupied spots"}), 400
    db.session.delete(lot)
    db.session.commit()
    cache.delete("admin_lots")
    return jsonify({"message": "Deleted"})


@admin_bp.get("/spots/<int:lot_id>")
@login_required
def lot_spots(lot_id):
    gate = _require_admin()
    if gate:
        return gate
    spots = ParkingSpot.query.filter_by(lot_id=lot_id).all()
    return jsonify([{"id": s.id, "status": s.status} for s in spots])


@admin_bp.get("/summary")
@login_required
def summary():
    gate = _require_admin()
    if gate:
        return gate
    lots = ParkingLot.query.all()
    data = []
    for lot in lots:
        total = ParkingSpot.query.filter_by(lot_id=lot.id).count()
        occupied = ParkingSpot.query.filter_by(lot_id=lot.id, status="O").count()
        data.append({"lot": lot.prime_location_name, "total": total, "occupied": occupied})
    return jsonify(data)



