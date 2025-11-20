def premium_discount(price: float) -> float:
    return price * 0.8


def student_discount(price: float) -> float:
    return price * 0.9


def parity_discount(price: float) -> float:
    return price * 0.75


def no_discount(price: float) -> float:
    return price


# Mapping van user_type naar functie
DISCOUNT_MAP = {
    "premium": premium_discount,
    "student": student_discount,
    "parity": parity_discount,
}


def apply_discount(price: float, user_type: str) -> float:
    discount_func = DISCOUNT_MAP.get(user_type, no_discount)
    return discount_func(price)


def main():
    prices = [100, 200, 300]
    user_type = "student"

    final_prices = [apply_discount(price, user_type) for price in prices]
    print(final_prices)


if __name__ == "__main__":
    main()
