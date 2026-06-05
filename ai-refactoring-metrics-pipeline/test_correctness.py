import pytest

from legacy_calculator import calculate_total as legacy_calc
from refactored_calculator import calculate_total as refactored_calc

TEST_CASES = [
    ([{'category': 'electronics', 'price': 1200}], None, 'premium', True),
    ([{'category': 'clothing', 'price': 50}], 'SUMMER', 'regular', False),
    ([{'category': 'books', 'price': 30}], 'VIP20', 'premium', False),
]


@pytest.mark.parametrize(
    "items,discount,customer,holiday",
    TEST_CASES
)
def test_refactored_matches_legacy(
    items,
    discount,
    customer,
    holiday
):
    legacy_result = legacy_calc(
        items,
        discount,
        customer,
        holiday
    )

    refactored_result = refactored_calc(
        items,
        discount,
        customer,
        holiday
    )

    assert abs(
        legacy_result - refactored_result
    ) < 0.01
