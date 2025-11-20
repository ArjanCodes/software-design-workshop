# Mapping van user_type naar korting
DISCOUNT_MAP = {
    "premium": 0.8,
    "student": 0.9,
    "parity": 0.75,
}


def apply_discount(price: float, user_type: str) -> float:
    discount = DISCOUNT_MAP.get(user_type, 1.0)
    return price * discount


def main():
    prices = [100, 200, 300]
    user_type = "student"

    final_prices = [apply_discount(price, user_type) for price in prices]
    print(final_prices)


if __name__ == "__main__":
    main()
