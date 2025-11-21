from main import checkout


def r2(x):
    return float(f"{x:.2f}")


# -----------------------------
# Basic subtotal tests
# -----------------------------


def test_simple_subtotal_no_discounts():
    cart = [{"name": "A", "category": "other", "unit_price": 10, "qty": 2}]
    res = checkout(cart)
    assert res["subtotal"] == 20
    assert res["discount"] == 0
    assert res["tax"] == r2(20 * 0.21)
    assert res["total"] == r2(20 + 20 * 0.21)
