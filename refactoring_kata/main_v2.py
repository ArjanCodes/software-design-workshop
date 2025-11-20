# after.py — clean checkout with minimal CategorySummary

from dataclasses import dataclass
from typing import Any

# ------------------------------
# CONSTANTS
# ------------------------------

BULK_QTY_THRESHOLD = 5
BULK_DISCOUNT_RATE = 0.10

FOOD_COUPON_THRESHOLD = 20.0
FOOD_COUPON_VALUE = 3.0

TAX_RATES = {
    "food": 0.06,
    "other": 0.21,
}


# ------------------------------
# ITEM MODEL
# ------------------------------


@dataclass
class Item:
    name: str
    category: str  # "food" or "other"
    unit_price: float
    qty: int

    @property
    def line_total(self) -> float:
        return self.unit_price * self.qty


# ------------------------------
# CATEGORY SUMMARY MODEL
# ------------------------------


@dataclass
class CategorySummary:
    subtotal: float  # original subtotal
    discount: float  # total discount (bulk + coupon)
    tax: float  # tax applied to (subtotal - discount)


# ------------------------------
# HELPER FUNCTIONS
# ------------------------------


def compute_subtotal(items: list[Item]) -> float:
    return sum(i.line_total for i in items)


def compute_bulk_discount(items: list[Item]) -> float:
    return sum(
        i.line_total * BULK_DISCOUNT_RATE for i in items if i.qty >= BULK_QTY_THRESHOLD
    )


def compute_category_coupon(category: str, subtotal: float) -> float:
    if category == "food" and subtotal >= FOOD_COUPON_THRESHOLD:
        return FOOD_COUPON_VALUE
    return 0.0


def compute_category_tax(category: str, amount: float) -> float:
    """Compute tax based on the discounted net amount."""
    return amount * TAX_RATES.get(category, 0.0)


# ------------------------------
# CORE LOGIC — ITEMS ONLY
# ------------------------------


def checkout_items(items: list[Item]) -> dict[str, float]:
    categories = ["food", "other"]

    # Each category will get exactly one CategorySummary
    category_summaries: list[CategorySummary] = []

    for cat in categories:
        category_items = [i for i in items if i.category == cat]
        subtotal = compute_subtotal(category_items)

        # compute total discount
        bulk = compute_bulk_discount(category_items)
        coupon = compute_category_coupon(cat, subtotal)
        discount = bulk + coupon

        # compute tax based on net = subtotal - discount
        tax = compute_category_tax(cat, subtotal - discount)

        category_summaries.append(
            CategorySummary(
                subtotal=subtotal,
                discount=discount,
                tax=tax,
            )
        )

    # aggregate summary totals
    subtotal_sum = sum(s.subtotal for s in category_summaries)
    discount_sum = sum(s.discount for s in category_summaries)
    tax_sum = sum(s.tax for s in category_summaries)

    # net total after discounts + tax
    total = (subtotal_sum - discount_sum) + tax_sum

    return {
        "subtotal": round(subtotal_sum, 2),
        "discount": round(discount_sum, 2),
        "tax": round(tax_sum, 2),
        "total": round(total, 2),
    }


# ------------------------------
# WRAPPER FOR DICT INPUT
# ------------------------------


def checkout(cart: list[dict[str, Any]]) -> dict[str, float]:
    items = [Item(**d) for d in cart]
    return checkout_items(items)
