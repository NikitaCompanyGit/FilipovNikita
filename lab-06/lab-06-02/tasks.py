# tasks.py
from functools import reduce, wraps


# Мы можем импортировать что-то из src, если нужно,
# но для чистоты решения задачи часто самодостаточны.
# Если нужно использовать декоратор из методички, то:
# from src.decorators import timer

# === Задание 1: Анализ студентов ===
def analyze_students(students_list):
    """
    Принимает список словарей студентов.
    Возвращает словарь со статистикой.
    """
    if not students_list:
        return None

    # Вычисляем сумму оценок через reduce
    total_grade = reduce(lambda acc, s: acc + s['grade'], students_list, 0)

    # Фильтруем отличников
    excellent_students = list(filter(lambda s: s['grade'] >= 90, students_list))

    return {
        'total_students': len(students_list),
        'average_grade': total_grade / len(students_list),
        'excellent_list': [s['name'] for s in excellent_students]
    }


# === Задание 2: Декоратор Логгер ===
def logger(func):
    """
    Логирует имя функции, аргументы и результат.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        # Формируем красивое отображение аргументов
        args_str = [repr(a) for a in args]
        kwargs_str = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_str + kwargs_str)

        print(f"[Logger] Call: {func.__name__}({signature})")

        result = func(*args, **kwargs)

        print(f"[Logger] Result: {result}")
        return result

    return wrapper


# === Задание 3: Генератор простых чисел ===
def prime_generator():
    """
    Бесконечный генератор простых чисел.
    """
    num = 2
    while True:
        is_prime = True
        for i in range(2, int(num ** 0.5) + 1):
            if num % i == 0:
                is_prime = False
                break

        if is_prime:
            yield num

        num += 1
