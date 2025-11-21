def handle_order(product_type: str, customer_name: str) -> None:
    if product_type == "ebook":
        print(f"Sending e-book to {customer_name}")
    elif product_type == "course":
        print(f"Enrolling {customer_name} in the course")
    elif product_type == "license":
        print(f"Generating license for {customer_name}")
    else:
        raise ValueError("Unknown product type")


def send_invoice(customer_name: str, amount: float) -> None:
    print(f"Sending invoice of €{amount} to {customer_name}")


def main() -> None:
    handle_order("ebook", "Alice")
    send_invoice("Alice", 29)
    handle_order("course", "Bob")
    send_invoice("Bob", 99)
    handle_order("license", "Charlie")
    send_invoice("Charlie", 49)


if __name__ == "__main__":
    main()
