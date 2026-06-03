def calculate_sum(a, b):
    """Calculate sum of two numbers."""
    result = a + b
    return result


def process_data(x):
    """Process data based on value."""
    if x > 0:
        print("Positive")
    else:
        print("Negative")


if __name__ == "__main__":
    print(calculate_sum(5, 10))
