from abc import ABC, abstractmethod
from typing import Dict, List, Optional


class DiscountStrategy(ABC):

    @abstractmethod
    def calculate_discount(
        self,
        price: float,
        customer_type: str,
        is_holiday: bool,
        discount_code: Optional[str] = None
    ) -> float:
        pass


class ElectronicsDiscountStrategy(DiscountStrategy):

    def calculate_discount(
        self,
        price: float,
        customer_type: str,
        is_holiday: bool,
        discount_code: Optional[str] = None
    ) -> float:

        if price > 1000:
            if customer_type == "premium":
                return price * (0.7 if is_holiday else 0.8)
            return price * (0.85 if is_holiday else 0.9)

        return price * (0.9 if customer_type == "premium" else 0.95)


class ClothingDiscountStrategy(DiscountStrategy):

    def calculate_discount(
        self,
        price: float,
        customer_type: str,
        is_holiday: bool,
        discount_code: Optional[str] = None
    ) -> float:

        if discount_code == "SUMMER":
            return price * (0.6 if customer_type == "premium" else 0.7)

        return price * (0.85 if customer_type == "premium" else 0.9)


class DefaultDiscountStrategy(DiscountStrategy):

    def calculate_discount(
        self,
        price: float,
        customer_type: str,
        is_holiday: bool,
        discount_code: Optional[str] = None
    ) -> float:

        return price * 0.9 if discount_code else price


def get_discount_strategy(category: str) -> DiscountStrategy:

    return {
        "electronics": ElectronicsDiscountStrategy(),
        "clothing": ClothingDiscountStrategy(),
    }.get(category, DefaultDiscountStrategy())


def calculate_total(
    items: List[Dict],
    discount_code: Optional[str],
    customer_type: str,
    is_holiday: bool
) -> float:

    total = 0

    for item in items:
        strategy = get_discount_strategy(item["category"])

        total += strategy.calculate_discount(
            item["price"],
            customer_type,
            is_holiday,
            discount_code
        )

    if discount_code == "VIP20":
        total *= 0.8

    return total


def process_order(order_data: Optional[Dict]) -> Optional[float]:

    if not order_data:
        return None

    items = order_data.get("items")

    if items is None:
        return None

    if len(items) == 0:
        return 0

    customer = order_data.get("customer")

    if customer is None:
        return None

    return calculate_total(
        items,
        order_data.get("discount_code"),
        customer.get("type"),
        order_data.get("is_holiday", False)
    )
