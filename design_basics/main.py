def apply_discount(price, user_type):
    if user_type == "premium":
        return price * 0.8
    elif user_type == "student":
        return price * 0.9
    elif user_type == "parity":
        return price * 0.75
    else:
        return price


def main():
    prices = [100, 200, 300]
    user_type = "student"

    final_prices = [apply_discount(price, user_type) for price in prices]
    print(final_prices)


if __name__ == "__main__":
    main()
