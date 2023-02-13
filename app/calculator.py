from datetime import datetime
import numpy as np
from .constants import Constants as c


class Calculator:
    """A class to calculate the delivery fee based on the given parameters."""

    def __init__(
        self,
        cart_value: int,
        delivery_distance: int,
        amount_of_items: int,
        time: datetime,
    ):
        self.cart_value = cart_value
        self.delivery_distance = delivery_distance
        self.amount_of_items = amount_of_items
        self.time = time
        self.delivery_fee = c.BASE_FEE
        self.calculate_total_delivery_fee()

    def get_delivery_fee(self) -> int:
        """Returns the delivery fee for customer.
        Returns:
            int: The delivery fee for customer
        """
        return self.delivery_fee

    def calculate_total_delivery_fee(self) -> None:
        """Calculates the total delivery fee for order."""
        self.calculate_small_order_fee()
        self.calculate_delivery_fee_by_distance()
        self.calculate_extra_fee_if_over_four_items()
        self.calculate_free_delivery_if_cart_value_more_than_100_euros()
        self.calculate_rush_hour_fee()
        self.calculate_maximum_delivery_fee()

    def calculate_small_order_fee(self) -> None:
        """This method finds if the cart value is under 10€
        and adds the remaining amount of the 10€ to the delivery price.
        If the cart value is over 10€, nothing is added.
        """
        self.delivery_fee += max(c.MIN_ORDER_VALUE - self.cart_value, 0)

    def calculate_delivery_fee_by_distance(self) -> None:
        """
        This method calculates the additional charges
        that apply when the delivery distance exceeds 1000 meters.
        Fee is added every 500 meters.
        """
        extra_distance = max(self.delivery_distance - c.DISTANCE_BEFORE_EXTRA_FEES, 0)
        sum_of_extra_fees = (
            int(np.ceil(extra_distance / c.DISTANCE_FOR_NEW_FEE)) * c.LONG_DISTANCE_FEE
        )
        self.delivery_fee += sum_of_extra_fees

    def calculate_extra_fee_if_over_four_items(self) -> None:
        """
        This method calculates the additional charges for extra items in
        that apply when the number of items is more than 4.
        If more than 12 items, bulk fee is added to the delivery price.
        """

        extra_items = np.maximum(self.amount_of_items - c.ITEMS_BEFORE_EXTRA_FEES, 0)
        sum_of_extra_fees = int(extra_items * c.EXTRA_ITEM_FEE)
        self.delivery_fee += sum_of_extra_fees

        if extra_items + c.ITEMS_BEFORE_EXTRA_FEES > 12:
            self.delivery_fee += c.BULK_FEE

    def calculate_free_delivery_if_cart_value_more_than_100_euros(self) -> None:
        """This method sets the delivery fee as 0€
        if the cart value is equal or more than 100€."""

        if self.cart_value >= c.FREE_DELIVERY_CART_VALUE:
            self.delivery_fee = 0

    def calculate_rush_hour_fee(self) -> None:
        """This method ensures that during the Friday rush (3 - 7 PM UTC),
        the total delivery fee will be multiplied by rush hour fee.
        """
        if self.time.weekday() == c.RUSH_DAY and self.time.hour in range(
            c.RUSH_START, c.RUSH_END
        ):
            self.delivery_fee = int(self.delivery_fee * c.RUSH_MULTIPLIER_FEE)

    def calculate_maximum_delivery_fee(self) -> None:
        """This method ensures that the delivery fee can never be more than 15€,
        including possible surcharges.
        """
        self.delivery_fee = min(self.delivery_fee, c.MAX_FEE)
