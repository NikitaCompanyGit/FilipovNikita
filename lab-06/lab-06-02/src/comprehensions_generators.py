# comprehensions_generators.py

def run_comprehension_demos():
    print("\n--- Demo: Comprehensions ---")
    numbers = [1, 2, 3, 4, 5]

    # List comprehension
    squares = [x * x for x in numbers]
    print(f"Squares list: {squares}")

    # Generator expression (ленивое вычисление)
    squares_gen = (x * x for x in numbers)
    print(f"Squares generator object: {squares_gen}")
    print(f"From generator: {list(squares_gen)}")


def fibonacci_generator(limit):
    """Генератор чисел Фибоначчи"""
    a, b = 0, 1
    count = 0
    while count < limit:
        yield a
        a, b = b, a + b
        count += 1
