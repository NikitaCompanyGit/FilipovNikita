# functions_as_objects.py

def square(x):
    return x * x


def cube(x):
    return x * x * x


def apply_function(func, value):
    """Применяет функцию к значению"""
    return func(value)


def create_multiplier(factor):
    """Создает функцию-умножитель (пример возврата функции)"""

    def multiplier(x):
        return x * factor

    return multiplier


# Этот блок выполнится только если запустить файл напрямую,
# а не импортировать его
if __name__ == "__main__":
    print("--- Demo: Functions as Objects ---")
    my_function = square
    print(f"square(5) = {square(5)}")
    print(f"my_function(5) = {my_function(5)}")

    double = create_multiplier(2)
    print(f"double(10) = {double(10)}")
