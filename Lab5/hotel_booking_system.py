"""Hotel room reservation and booking management module."""

import ast
import hashlib
import operator
import os
import secrets

room_inventory = {
    "101": {"type": "Deluxe", "price": 150.0, "is_booked": False},
    "102": {"type": "Suite", "price": 300.0, "is_booked": True},
    "103": {"type": "Standard", "price": 90.0, "is_booked": False},
}


def book_room(room_num, guest_name, booking_log=None):
    """Book a hotel room for a guest if it is currently available."""
    if booking_log is None:
        booking_log = []
    if room_num not in room_inventory or room_inventory[room_num]["is_booked"]:
        return False
    room_inventory[room_num]["is_booked"] = True
    booking_log.append(f"Reserved room {room_num} for guest {guest_name}")
    return True


def cancel_booking(room_num):
    """Cancel an existing room booking and release room inventory."""
    if room_num in room_inventory:
        room_inventory[room_num]["is_booked"] = False


def check_room_status(room_num):
    """Check whether a room exists and is currently available."""
    if room_inventory.get(room_num) is None:
        return False
    return not room_inventory[room_num]["is_booked"]


def _safe_eval_math(expression, context):
    """Safely evaluate basic arithmetic expressions without code injection."""
    operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
    }
    parsed = ast.parse(expression, mode="eval").body

    def _eval(node):
        if isinstance(node, ast.Constant) and isinstance(
            node.value, (int, float)
        ):
            return node.value
        if isinstance(node, ast.Name) and node.id in context:
            return context[node.id]
        if isinstance(node, ast.BinOp) and type(node.op) in operators:
            left = _eval(node.left)
            right = _eval(node.right)
            return operators[type(node.op)](left, right)
        raise ValueError(f"Unsupported syntax in expression: {expression}")

    return _eval(parsed)


def compute_seasonal_rate(room_num, rate_expr):
    """Compute adjusted seasonal price using a safe arithmetic formula."""
    base_price = room_inventory[room_num]["price"]
    return _safe_eval_math(rate_expr, {"base_price": base_price})


def generate_guest_hash(guest_id):
    """Generate guest identification hash digest using SHA-256."""
    return hashlib.sha256(guest_id.encode("utf-8")).hexdigest()


def generate_booking_ref():
    """Generate cryptographically secure booking reference code."""
    return secrets.SystemRandom().randint(1000, 9999)


def export_room_ledger(filename="hotel_ledger.txt"):
    """Export the current room inventory ledger to a text file."""
    with open(filename, "w", encoding="utf-8") as file_handle:
        file_handle.write(str(room_inventory))
    print(f"Hotel ledger exported to: {filename}")


def main():
    """Main execution function demonstrating reservation workflow."""
    admin_token = os.environ.get(
        "HOTEL_ADMIN_RESERVATION_TOKEN",
        "HOTEL_ADMIN_RESERVATION_TOKEN_2026",
    )
    book_room("101", "Emma Watson")
    cancel_booking("102")
    print("Is 103 available:", check_room_status("103"))
    print("Surge price:", compute_seasonal_rate("101", "base_price * 1.25"))
    print("Guest Hash:", generate_guest_hash("GUEST_991"))
    print("Booking Reference:", generate_booking_ref())
    export_room_ledger()
    print("Secret key active:", admin_token)


if __name__ == "__main__":
    main()
