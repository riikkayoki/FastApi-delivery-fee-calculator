import unittest
from datetime import datetime
from app.calculator import Calculator


class TestCalculator(unittest.TestCase):
    def setUp(self) -> None:

        self.friday_is_rush = datetime.fromisoformat("2022-11-25T15:00:00+00:01")
        self.not_friday_but_is_rush_hour = datetime.fromisoformat(
            "2022-11-24T12:15:00+00:00"
        )
        self.friday_is_not_rush = datetime.fromisoformat("2022-11-25T12:00:00+00:00")

    """Tests for small order fee"""

    def test_small_order_fee_cart_value_under_1000(self) -> None:
        calculator = Calculator(900, 0, 1, self.friday_is_not_rush)
        actual_fee = calculator.get_delivery_fee()
        expected_fee = 300
        self.assertEqual(actual_fee, expected_fee)

    def test_small_order_fee_cart_value_is_1000(self) -> None:
        calculator = Calculator(1000, 0, 1, self.friday_is_not_rush)
        actual_fee = calculator.get_delivery_fee()
        expected_fee = 200
        self.assertEqual(actual_fee, expected_fee)

    def test_small_order_fee_cart_value_is_over_1000(self) -> None:
        calculator = Calculator(1200, 0, 1, self.friday_is_not_rush)
        actual_fee = calculator.get_delivery_fee()
        expected_fee = 200
        self.assertEqual(actual_fee, expected_fee)

    """Tests for delivery distance fee"""

    def test_delivery_fee_when_distance_first_1000_km(self) -> None:
        calculator = Calculator(1000, 1000, 1, self.friday_is_not_rush)
        actual_fee = calculator.get_delivery_fee()
        expected_fee = 200
        self.assertEqual(actual_fee, expected_fee)

    def test_delivery_fee_when_distance_over_1000_km(self) -> None:
        calculator = Calculator(1000, 1001, 1, self.friday_is_not_rush)
        actual_fee = calculator.get_delivery_fee()
        expected_fee = 300
        self.assertEqual(actual_fee, expected_fee)

    def test_delivery_fee_when_distance_is_1500_km(self) -> None:
        calculator = Calculator(1000, 1500, 1, self.friday_is_not_rush)
        actual_fee = calculator.get_delivery_fee()
        expected_fee = 300
        self.assertEqual(actual_fee, expected_fee)

    def test_delivery_fee_when_distance_over_1500(self) -> None:
        calculator = Calculator(1000, 1501, 1, self.friday_is_not_rush)
        actual_fee = calculator.get_delivery_fee()
        expected_fee = 400
        self.assertEqual(actual_fee, expected_fee)

    """Tests for cart item fees"""

    def test_delivery_fee_under_5_items(self) -> None:
        calculator = Calculator(1000, 0, 4, self.friday_is_not_rush)
        actual_fee = calculator.get_delivery_fee()
        expected_fee = 200
        self.assertEqual(actual_fee, expected_fee)

    def test_delivery_fee_5_items(self) -> None:
        calculator = Calculator(1000, 0, 5, self.friday_is_not_rush)
        actual_fee = calculator.get_delivery_fee()
        expected_fee = 250
        self.assertEqual(actual_fee, expected_fee)

    def test_delivery_fee_over_5_items(self) -> None:
        calculator = Calculator(1000, 0, 10, self.friday_is_not_rush)
        actual_fee = calculator.get_delivery_fee()
        expected_fee = 500
        self.assertEqual(actual_fee, expected_fee)

    def test_delivery_fee_over_12_items(self) -> None:
        calculator = Calculator(1000, 0, 13, self.friday_is_not_rush)
        actual_fee = calculator.get_delivery_fee()
        expected_fee = 770
        self.assertEqual(actual_fee, expected_fee)

    """Tests for cart value fee"""

    def test_free_delivery_if_cart_value_under_100_euros(self) -> None:
        calculator = Calculator(9999, 0, 1, self.friday_is_not_rush)
        actual_fee = calculator.get_delivery_fee()
        expected_fee = 200
        self.assertEqual(actual_fee, expected_fee)

    def test_free_delivery_if_cart_value_is_100_euros(self) -> None:
        calculator = Calculator(10000, 10000, 10, self.friday_is_not_rush)
        actual_fee = calculator.get_delivery_fee()
        expected_fee = 0
        self.assertEqual(actual_fee, expected_fee)

    def test_free_delivery_if_cart_value_is_over_100_euros(self) -> None:
        calculator = Calculator(15000, 2000, 10, self.friday_is_rush)
        actual_fee = calculator.get_delivery_fee()
        expected_fee = 0
        self.assertEqual(actual_fee, expected_fee)

    # """Tests for rush hour fees"""

    def test_rush_hour_fee_when_rush_hour(self) -> None:
        calculator = Calculator(1000, 999, 4, self.friday_is_rush)
        actual_fee = calculator.get_delivery_fee()
        expected_fee = 240
        self.assertEqual(actual_fee, expected_fee)

    def test_rush_hour_fee_when_friday_but_not_rush_hour(self) -> None:
        calculator = Calculator(1000, 999, 4, self.friday_is_not_rush)
        actual_fee = calculator.get_delivery_fee()
        expected_fee = 200
        self.assertEqual(actual_fee, expected_fee)

    def test_rush_hour_fee_when_not_friday_but_is_rush_hour(self) -> None:
        calculator = Calculator(1000, 999, 4, self.not_friday_but_is_rush_hour)
        actual_fee = calculator.get_delivery_fee()
        expected_fee = 200
        self.assertEqual(actual_fee, expected_fee)

    """Tests for maximum fee"""

    def test_maximum_delivery_fee_when_the_amounts_would_exceed_15_euros(self) -> None:
        calculator = Calculator(50, 30000, 100, self.friday_is_rush)
        actual_fee = calculator.get_delivery_fee()
        expected_fee = 1500
        self.assertEqual(actual_fee, expected_fee)
