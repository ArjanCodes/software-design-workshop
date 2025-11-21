from abc import ABC, abstractmethod


class DiscountStrategy(ABC):
    @abstractmethod
    def apply(self, price: float) -> float:
        pass


class PremiumDiscount(DiscountStrategy):
    def apply(self, price: float) -> float:
        return price * 0.8


class StudentDiscount(DiscountStrategy):
    def apply(self, price: float) -> float:
        return price * 0.9


class ParityDiscount(DiscountStrategy):
    def apply(self, price: float) -> float:
        return price * 0.75


class NoDiscount(DiscountStrategy):
    def apply(self, price: float) -> float:
        return price


def get_discount_strategy(user_type: str) -> DiscountStrategy:
    strategies = {
        "premium": PremiumDiscount(),
        "student": StudentDiscount(),
        "parity": ParityDiscount(),
    }
    return strategies.get(user_type, NoDiscount())


def main():
    prices = [100, 200, 300]
    user_type = "student"

    final_prices = [get_discount_strategy(user_type).apply(price) for price in prices]
    print(final_prices)


if __name__ == "__main__":
    main()
