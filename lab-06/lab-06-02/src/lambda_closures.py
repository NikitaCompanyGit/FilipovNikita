# lambda_closures.py

def run_lambda_demos():
    print("\n--- Demo: Lambda Functions ---")
    numbers = [1, 2, 3, 4, 5]

    # Lambda с map
    squares = list(map(lambda x: x * x, numbers))
    print(f"Squares (lambda): {squares}")

    # Lambda с filter
    evens = list(filter(lambda x: x % 2 == 0, numbers))
    print(f"Evens (lambda): {evens}")


def create_counter():
    """Создает счетчик с замыканием"""
    count = 0

    def counter():
        nonlocal count
        count += 1
        return count

    return counter
