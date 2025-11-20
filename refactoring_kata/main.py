def checkout(cart):
    subtotal = 0
    tax = 0
    food_sub = 0

    # first pass: compute subtotals
    for item in cart:
        line_total = item["unit_price"] * item["qty"]
        subtotal += line_total

        if item["category"] == "food":
            food_sub += line_total

    # second pass: compute bulk discounts
    food_bulk = 0
    other_bulk = 0
    for item in cart:
        if item["qty"] >= 5:
            lt = item["unit_price"] * item["qty"]
            if item["category"] == "food":
                food_bulk += lt * 0.10
            else:
                other_bulk += lt * 0.10

    # coupon only for food
    food_coupon = 0
    if food_sub >= 20:
        food_coupon = 3.0

    # compute nets
    food_net = food_sub - (food_bulk + food_coupon)
    other_net = subtotal - food_sub - other_bulk

    # food taxed at 6% and other at 21%
    if food_net < 0:
        tmp_food_net = 0
    else:
        tmp_food_net = food_net

    if other_net < 0:
        tmp_other_net = 0
    else:
        tmp_other_net = other_net

    food_tax = tmp_food_net * 0.06
    other_tax = tmp_other_net * 0.21
    tax = food_tax + other_tax

    return {
        "subtotal": round(
            food_net + other_net + food_bulk + other_bulk + food_coupon, 2
        ),
        "discount": round(food_bulk + other_bulk + food_coupon, 2),
        "tax": round(tax, 2),
        "total": round((food_net + other_net) + tax, 2),
    }
