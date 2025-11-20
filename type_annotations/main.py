def filter_odd_numbers(numbers):
    """Filters odd numbers from a sequence of numbers."""
    return [num for num in numbers if num % 2 == 0]


def square_numbers(numbers):
    """Square numbers in a sequence."""
    return [num**2 for num in numbers]


def count_chars(words):
    """Counts the number of characters in a sequence of words."""
    return [len(word) for word in words]


def process_data(
    data,
    process_func,
    filter_func=None,
):
    """Applies filter_func and process_func on a data sequence."""
    if filter_func:
        data = filter_func(data)
    return process_func(data)


def main():
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    result = process_data(numbers, square_numbers, filter_odd_numbers)
    print(result)

    words = ["apple", "banana", "cherry"]
    result2 = process_data(words, process_func=count_chars)
    print(result2)


if __name__ == "__main__":
    main()
