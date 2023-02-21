"""Измерение времени выполнения функции"""
import asyncio
import functools
import inspect
import logging
import os
import time
from contextlib import contextmanager


def duration(func):
    """Декоратор для вычисления времени выполнения функции/метода"""

    @contextmanager
    def wrapping_logic():
        func_name = f'{get_func_file(func)}:{func.__name__}'
        logging.debug('[start][%s]', func_name)
        start_ts = time.time()
        yield
        total_time = time.time() - start_ts
        logging.debug('[end][%s] time %.4f seconds', func_name, total_time)

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not asyncio.iscoroutinefunction(func):
            with wrapping_logic():
                return func(*args, **kwargs)
        else:
            async def tmp():
                with wrapping_logic():
                    return await func(*args, **kwargs)

            return tmp()

    return wrapper


def get_func_file(func) -> str:
    """Получение расположение файла"""
    return os.path.relpath(inspect.getfile(func))
