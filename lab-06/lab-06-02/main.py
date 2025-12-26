# main.py

# Импортируем модули из пакета src
import src.functions_as_objects as fao
import src.lambda_closures as lc
import src.higher_order as ho
import src.comprehensions_generators as cg
import src.decorators as dec

# Импортируем решения задач (лежит рядом)
import tasks


def main():
    print("==========================================")
    print("   LAB 6: PYTHON FUNCTIONAL PROGRAMMING   ")
    print("==========================================\n")

    # --- 1. Теория: Функции как объекты ---
    print(">>> 1. Functions as Objects")
    print(f"Square of 5: {fao.apply_function(fao.square, 5)}")
    triple = fao.create_multiplier(3)
    print(f"Triple of 10: {triple(10)}")

    # --- 2. Теория: Lambda и Замыкания ---
    lc.run_lambda_demos()
    print("\n>>> Closures")
    counter1 = lc.create_counter()
    print(f"Counter calls: {counter1()}, {counter1()}, {counter1()}")

    # --- 3. Теория: Функции высшего порядка ---
    ho.run_higher_order_demos()

    # --- 4. Теория: Генераторы ---
    cg.run_comprehension_demos()
    print("Fibonacci first 5:", list(cg.fibonacci_generator(5)))

    # --- 5. Теория: Декораторы ---
    print("\n>>> 5. Decorators")

    @dec.timer
    def slow_add(a, b):
        import time
        time.sleep(0.1)
        return a + b

    slow_add(10, 20)

    print("\n==========================================")
    print("         PRACTICAL TASKS RESULTS          ")
    print("==========================================\n")

    # --- Проверка Задания 1 ---
    print("Task 1: Student Analysis")
    # Берем список студентов из модуля higher_order внутри src
    stats = tasks.analyze_students(ho.students)
    print(f"Result: {stats}")

    # --- Проверка Задания 2 ---
    print("\nTask 2: Logger Decorator")

    @tasks.logger
    def power(x, y):
        return x ** y

    power(2, 3)

    # --- Проверка Задания 3 ---
    print("\nTask 3: Prime Number Generator")
    pg = tasks.prime_generator()
    print("First 10 primes generated:")
    for _ in range(10):
        print(next(pg), end=" ")
    print()


if __name__ == "__main__":
    main()
