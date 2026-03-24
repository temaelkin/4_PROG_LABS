import functools
from typing import *


def is_fibonacci(n: int) -> bool:
    """
    Проверяет, является ли число числом Фибоначчи.

    Args:
        n (int): Проверяемое число.

    Returns:
        bool: True, если число является числом Фибоначчи, иначе False.
    """

    if n < 0:
        return False

    a, b = 0, 1
    while a < n:
        a, b = b, a + b

    return a == n


class FibonacciLst:
    """
    Итератор, фильтрующий числа Фибоначчи из переданной последовательности.

    Использует протокол итератора (__iter__ и __next__).
    Возвращает только те элементы, которые являются числами Фибоначчи.

    Attributes:
        instance (List[Any]): Исходная последовательность для фильтрации.
        idx (int): Текущая позиция в последовательности.
    """

    def __init__(self, instance: List[Any]) -> None:
        """
        Инициализирует итератор.

        Args:
            instance (List[Any]): Последовательность для фильтрации.
        """

        self.instance = instance
        self.idx = 0

    def __iter__(self) -> 'FibonacciLst':
        """
        Возвращает сам объект итератора.

        Returns:
            FibonacciLst: Сам объект итератора.
        """

        return self

    def __next__(self) -> Any:
        """
        Возвращает следующее число Фибоначчи из последовательности.

        Raises:
            StopIteration: Когда достигнут конец последовательности.

        Returns:
            Any: Следующее число Фибоначчи.
        """

        while True:
            try:
                res = self.instance[self.idx]

            except IndexError:
                raise StopIteration

            if is_fibonacci(res):
                self.idx += 1
                return res

            self.idx += 1


class FibonacciLstSimple:
    """
    Итерируемый объект, фильтрующий числа Фибоначчи через __getitem__.

    В отличие от итератора, позволяет многократную итерацию и доступ по индексу.
    Каждый вызов __getitem__ сканирует последовательность с начала.

    Attributes:
        instance (List[Any]): Исходная последовательность для фильтрации.
    """

    def __init__(self, instance: List[Any]) -> None:
        """
        Инициализирует итерируемый объект.

        Args:
            instance (List[Any]): Последовательность для фильтрации.
        """

        self.instance = instance

    def __getitem__(self, idx: int) -> Any:
        """
        Возвращает число Фибоначчи по индексу в отфильтрованной последовательности.

        Args:
            idx (int): Индекс в отфильтрованной последовательности.

        Raises:
            IndexError: Если индекс выходит за пределы отфильтрованной последовательности.

        Returns:
            Any: Число Фибоначчи по указанному индексу.
        """

        count = 0
        for item in self.instance:
            if is_fibonacci(item):
                if count == idx:
                    return item
                count += 1

        raise IndexError


def fib_gen() -> Generator[List[int], int, None]:
    """
    Сопрограмма-генератор для генерации последовательности Фибоначчи.

    Принимает через send() количество чисел для генерации и возвращает список.
    Является бесконечным генератором.

    Yields:
        List[int]: Список чисел Фибоначчи.

    Receives:
        int: Количество чисел Фибоначчи для генерации.

    Returns:
        None: Генератор никогда не завершается (бесконечный цикл).
    """

    res = None

    while True:
        num = yield res
        res = []
        a = 0
        b = 1
        while num > 0:
            res.append(a)
            a, b = b, a + b
            num -= 1


def start(g):
    """
    Декоратор для автоматической инициализации генераторов-сопрограмм.

    Args:
        g: Функция-генератор для декорирования.

    Returns:
        Обёрнутая функция, возвращающая уже инициализированный генератор.
    """

    @functools.wraps(g)
    def inner(*args, **kwargs):
        gen = g(*args, **kwargs)
        next(gen)
        return gen

    return inner
