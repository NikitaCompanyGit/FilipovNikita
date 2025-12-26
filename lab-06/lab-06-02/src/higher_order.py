# higher_order.py
from functools import reduce

# Данные для работы (используются и в других модулях)
students = [
    {'name': 'Alice', 'grade': 85, 'age': 20},
    {'name': 'Bob', 'grade': 92, 'age': 22},
    {'name': 'Charlie', 'grade': 78, 'age': 19},
    {'name': 'Diana', 'grade': 95, 'age': 21},
    {'name': 'Eve', 'grade': 88, 'age': 20}
]

def run_higher_order_demos():
    print("\n--- Demo: Higher Order Functions ---")
    numbers = [1, 2, 3, 4, 5]

    # Map
    names = list(map(lambda s: s['name'], students))
    print(f"Names: {names}")

    # Reduce
    product = reduce(lambda x, y: x * y, numbers)
    print(f"Product of {numbers}: {product}")
