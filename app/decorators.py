# app/decorators.py
import time
from functools import wraps
from typing import Callable


def timer(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = (time.time() - start) * 1000
        print(f"  [{func.__name__}] {elapsed:.1f}ms")
        return result

    return wrapper


def require_role(role: str) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            current_role = kwargs.get("current_role", "guest")
            if current_role != role:
                raise PermissionError(f"Cần quyền '{role}', hiện tại: '{current_role}'")
            return func(*args, **kwargs)

        return wrapper

    return decorator
