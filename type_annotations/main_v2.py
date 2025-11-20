from typing import Callable, Iterable, Sized, SupportsFloat


def filter_odd_numbers(numbers: Iterable[int]) -> list[int]:
    """Filters odd numbers from a sequence of numbers."""
    return [num for num in numbers if num % 2 == 0]


def square_numbers(numbers: Iterable[SupportsFloat]) -> list[float]:
    """Square numbers in a sequence."""
    return [num**2 for num in numbers]


def count_elements(words: Iterable[Sized]) -> list[int]:
    """Counts the number of elements in an iterable of words."""
    return [len(word) for word in words]


type FilterFunc[T] = Callable[[T], T]
type ProcessFunc[T, V] = Callable[[T], V]


def process_data[T, V](
    data: T,
    process_func: ProcessFunc[T, V],
    filter_func: FilterFunc[T] | None = None,
) -> V:
    """Applies filter_func and process_func on a data sequence."""
    if filter_func:
        data = filter_func(data)
    return process_func(data)


def main() -> None:
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    result = process_data(
        numbers, process_func=square_numbers, filter_func=filter_odd_numbers
    )
    print(result)

    words = ["apple", "banana", "cherry"]
    result2 = process_data(words, process_func=count_elements)
    print(result2)


if __name__ == "__main__":
    main()
