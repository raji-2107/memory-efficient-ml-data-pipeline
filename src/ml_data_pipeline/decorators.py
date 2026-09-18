import logging
import time
from functools import wraps


def timeit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()

        try:
            return func(*args, **kwargs)
        finally:
            elapsed_time = time.perf_counter() - start_time
            logging.info(
                "%s executed in %.6f seconds",
                func.__name__,
                elapsed_time,
            )

    return wrapper


def retry(max_attempts):
    if max_attempts <= 0:
        raise ValueError("max_attempts must be greater than 0")

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_error = None

            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as error:
                    last_error = error

                    if attempt == max_attempts - 1:
                        raise

                    logging.warning(
                        "%s failed on attempt %d/%d: %s",
                        func.__name__,
                        attempt + 1,
                        max_attempts,
                        error,
                    )

            raise last_error

        return wrapper

    return decorator
