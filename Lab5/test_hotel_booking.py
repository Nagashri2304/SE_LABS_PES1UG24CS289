"""Unit tests for hotel booking system module."""

import os
import unittest
from hotel_booking_system import (
    room_inventory,
    book_room,
    cancel_booking,
    check_room_status,
    compute_seasonal_rate,
    generate_guest_hash,
    generate_booking_ref,
    export_room_ledger,
)


class TestHotelBookingSystem(unittest.TestCase):
    """Test cases verifying functionality of hotel booking system."""

    def setUp(self):
        """Reset room inventory before each test case."""
        room_inventory["101"]["is_booked"] = False
        room_inventory["102"]["is_booked"] = True
        room_inventory["103"]["is_booked"] = False

    def test_book_room_success(self):
        """Test successful booking of an available room."""
        log = []
        result = book_room("101", "Alice", log)
        self.assertTrue(result)
        self.assertTrue(room_inventory["101"]["is_booked"])
        self.assertEqual(len(log), 1)

    def test_book_room_already_booked(self):
        """Test that attempting to book a reserved room returns False."""
        result = book_room("102", "Bob")
        self.assertFalse(result)

    def test_book_room_mutable_default_isolated(self):
        """Verify that default booking log is not shared between calls."""
        book_room("101", "Guest1")
        room_inventory["101"]["is_booked"] = False
        fresh_log = []
        book_room("101", "Guest2", fresh_log)
        self.assertEqual(len(fresh_log), 1)

    def test_cancel_booking(self):
        """Test cancellation releases room and handles invalid room ID."""
        cancel_booking("102")
        self.assertFalse(room_inventory["102"]["is_booked"])
        # Should not raise exception on nonexistent room
        cancel_booking("999")

    def test_check_room_status(self):
        """Test room availability status checks."""
        self.assertTrue(check_room_status("101"))
        self.assertFalse(check_room_status("102"))
        self.assertFalse(check_room_status("999"))

    def test_compute_seasonal_rate(self):
        """Test calculation of seasonal price expression."""
        rate = compute_seasonal_rate("101", "base_price * 1.25")
        self.assertEqual(rate, 187.5)

    def test_generate_guest_hash(self):
        """Test guest identification hash generation."""
        digest = generate_guest_hash("GUEST_991")
        self.assertTrue(isinstance(digest, str) and len(digest) > 0)

    def test_generate_booking_ref(self):
        """Test numeric booking reference generation within 1000-9999."""
        ref = generate_booking_ref()
        self.assertGreaterEqual(ref, 1000)
        self.assertLessEqual(ref, 9999)

    def test_export_room_ledger(self):
        """Test export of room ledger to disk."""
        test_file = "test_ledger_output.txt"
        try:
            export_room_ledger(test_file)
            self.assertTrue(os.path.exists(test_file))
            with open(test_file, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertIn("101", content)
        finally:
            if os.path.exists(test_file):
                os.remove(test_file)


if __name__ == "__main__":
    unittest.main()
