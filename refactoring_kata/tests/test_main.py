from main_v2 import checkout


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


# -----------------------------
# Bulk discount tests (qty >= 5)
# -----------------------------


def test_bulk_discount_triggered():
    cart = [{"name": "Widget", "category": "other", "unit_price": 5, "qty": 5}]
    res = checkout(cart)

    original = 25  # 5*5
    bulk = original * 0.10  # 10% discount

    taxable = original - bulk
    expected_tax = taxable * 0.21

    expected_total = r2(original - bulk + expected_tax)

    assert res["discount"] == r2(bulk)
    assert res["tax"] == r2(expected_tax)
    assert res["total"] == expected_total


def test_bulk_no_trigger_below_threshold():
    cart = [{"name": "Widget", "category": "other", "unit_price": 5, "qty": 4}]
    res = checkout(cart)

    original = 20
    taxable = original
    expected_tax = taxable * 0.21

    assert res["discount"] == 0
    assert res["tax"] == r2(expected_tax)
    assert res["total"] == r2(original + expected_tax)


# -----------------------------
# Food coupon tests (€3 off if food total >= 20)
# -----------------------------


def test_food_coupon_applies_exact_20():
    cart = [
        {"name": "Milk", "category": "food", "unit_price": 4, "qty": 5}  # 20 total
    ]
    res = checkout(cart)

    original = 20
    bulk = original * 0.10  # qty >= 5 → bulk applies
    coupon = 3

    taxable = original - bulk - coupon
    expected_tax = taxable * 0.06

    expected_total = r2(original - bulk - coupon + expected_tax)

    assert res["discount"] == r2(bulk + coupon)
    assert res["tax"] == r2(expected_tax)
    assert res["total"] == expected_total


def test_food_coupon_does_not_apply_below_20():
    cart = [
        {"name": "Milk", "category": "food", "unit_price": 3.5, "qty": 5}  # 17.5
    ]
    res = checkout(cart)

    original = 17.5
    bulk = original * 0.10
    taxable = original - bulk
    expected_tax = taxable * 0.06

    assert res["discount"] == r2(bulk)  # no coupon
    assert res["tax"] == r2(expected_tax)
    assert res["total"] == r2(taxable + expected_tax)


# -----------------------------
# Tax tests for mixed carts
# -----------------------------


def test_mixed_food_and_other_correct_tax():
    cart = [
        {"name": "Pasta", "category": "food", "unit_price": 4, "qty": 5},  # 20 food
        {
            "name": "Notebook",
            "category": "other",
            "unit_price": 10,
            "qty": 2,
        },  # 20 other
    ]
    res = checkout(cart)

    # Expected values using the clean/category logic

    # --- Subtotals ---
    food_subtotal = 20
    other_subtotal = 20

    # --- Discounts ---
    food_bulk = 20 * 0.10  # 2.0
    food_coupon = 3.0  # coupon applies (>= 20)
    food_discount = food_bulk + food_coupon  # 5.0

    other_discount = 0.0  # no bulk, no coupon

    # --- Nets ---
    food_net = food_subtotal - food_discount  # 15
    other_net = other_subtotal - other_discount  # 20

    # --- Taxes ---
    expected_food_tax = food_net * 0.06  # 0.9
    expected_other_tax = other_net * 0.21  # 4.2
    expected_total_tax = round(expected_food_tax + expected_other_tax, 2)

    expected_total = round((food_net + other_net) + expected_total_tax, 2)

    assert res["subtotal"] == 40.00
    assert res["discount"] == 5.00
    assert res["tax"] == expected_total_tax  # 5.10
    assert res["total"] == expected_total  # 40 - 5 + 5.1 = 40.1


def test_tax_only_food_items():
    cart = [
        {
            "name": "Rice",
            "category": "food",
            "unit_price": 2,
            "qty": 10,
        },  # 20 total → coupon applies
    ]
    res = checkout(cart)

    food = 20
    bulk = food * 0.10  # qty >= 5
    coupon = 3
    taxable = food - bulk - coupon

    expected_tax = taxable * 0.06
    expected_total = r2(taxable + expected_tax)

    assert res["tax"] == r2(expected_tax)
    assert res["total"] == expected_total


def test_tax_only_other_items():
    cart = [
        {"name": "Chair", "category": "other", "unit_price": 12, "qty": 3},
    ]
    res = checkout(cart)

    subtotal = 36
    taxable = subtotal
    expected_tax = taxable * 0.21
    expected_total = round(taxable + expected_tax, 2)

    assert res["tax"] == r2(expected_tax)
    assert res["total"] == expected_total


def test_tax_mixed_no_discounts():
    cart = [
        {"name": "Apple", "category": "food", "unit_price": 3, "qty": 3},  # 9
        {"name": "Pen", "category": "other", "unit_price": 2, "qty": 2},  # 4
    ]
    res = checkout(cart)

    food = 9
    other = 4
    expected_tax = food * 0.06 + other * 0.21
    expected_total = r2(food + other + expected_tax)

    assert res["tax"] == r2(expected_tax)
    assert res["total"] == expected_total


# -----------------------------
# Correct subtotal reconstruction
# -----------------------------


def test_subtotal_reconstructed_correctly():
    cart = [
        {"name": "A", "category": "other", "unit_price": 5, "qty": 5},  # 25, bulk 2.5
        {
            "name": "B",
            "category": "food",
            "unit_price": 4,
            "qty": 5,
        },  # 20, bulk 2, coupon 3
    ]
    res = checkout(cart)

    assert res["subtotal"] == 45  # 25 + 20
