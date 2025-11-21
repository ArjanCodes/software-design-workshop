from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class ProductOrder(ABC):
    customer_name: str
    invoice_amount: float

    @abstractmethod
    def process(self) -> None:
        pass


class EbookOrder(ProductOrder):
    def process(self) -> None:
        print(f"Sending e-book to {self.customer_name}")


class CourseOrder(ProductOrder):
    def process(self) -> None:
        print(f"Enrolling {self.customer_name} in the course")


class LicenseOrder(ProductOrder):
    def process(self) -> None:
        print(f"Generating license for {self.customer_name}")


def send_invoice(order: ProductOrder) -> None:
    print(f"Sending invoice of €{order.invoice_amount} to {order.customer_name}")


def main() -> None:
    # Factory-functie of DI zou dit in praktijk doen:
    orders = [
        EbookOrder("Alice", 29),
        CourseOrder("Bob", 99),
        LicenseOrder("Charlie", 49),
    ]

    for order in orders:
        order.process()
        send_invoice(order)


if __name__ == "__main__":
    main()
