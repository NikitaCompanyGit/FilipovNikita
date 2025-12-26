# decorators.py
import time
from functools import wraps

def timer(func):
    """Декоратор для измерения времени выполнения"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"[Timer] {func.__name__} took {end - start:.6f} sec")
        return result
    return wrapper

def repeat(num_times=2):
    """Декоратор с параметром для повтора выполнения"""
    def decorator_repeat(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(num_times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator_repeat

def cache(func):
    """Декоратор для кэширования результатов (Memoization)"""
    memo = {}
    @wraps(func)
    def wrapper(*args):
        if args in memo:
            print(f"[Cache] Fetching result for {args}")
            return memo[args]
        result = func(*args)
        memo[args] = result
        return result
    return wrapper
