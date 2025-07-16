import time
import functools
import asyncio

def timed(name: str = None):
    def decorator(func):
        is_coroutine = asyncio.iscoroutinefunction(func)

        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = await func(*args, **kwargs)
            duration = time.perf_counter() - start
            print(f"[{name or func.__name__}] completed in {duration:.4f} sec")
            return result

        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = func(*args, **kwargs)
            duration = time.perf_counter() - start
            print(f"[{name or func.__name__}] completed in {duration:.4f} sec")
            return result

        return async_wrapper if is_coroutine else sync_wrapper

    return decorator
