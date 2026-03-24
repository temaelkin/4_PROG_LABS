import unittest
from main import is_fibonacci, FibonacciLst, FibonacciLstSimple

class FibonacciTest(unittest.TestCase):
    def test_is_fibonacci_positive_cases(self):
        """Тест: функция корректно определяет числа Фибоначчи."""
        fibonacci_numbers = [0, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144]
        for num in fibonacci_numbers:
            with self.subTest(num=num):
                self.assertTrue(
                    is_fibonacci(num),
                    f"{num} должно быть числом Фибоначчи"
                )

    def test_is_fibonacci_negative_cases(self):
        """Тест: функция корректно отклоняет не-числа Фибоначчи."""
        non_fibonacci_numbers = [4, 6, 7, 9, 10, 11, 12, 14, 15, 100, 1000]
        for num in non_fibonacci_numbers:
            with self.subTest(num=num):
                self.assertFalse(
                    is_fibonacci(num),
                    f"{num} не должно быть числом Фибоначчи"
                )

    def test_fibonacci_lst_iterator(self):
        """Тест: итератор FibonacciLst корректно фильтрует последовательность."""
        test_list = list(range(30))
        expected = [0, 1, 2, 3, 5, 8, 13, 21]
        result = list(FibonacciLst(test_list))
        self.assertEqual(
            result,
            expected,
            f"Итератор должен вернуть {expected}, получил {result}"
        )

    def test_fibonacci_lst_simple_getitem(self):
        """Тест: класс FibonacciLstSimple корректно работает с __getitem__."""
        test_list = [0, 1, 2, 4, 5, 7, 8, 10, 13, 20]
        fib_filter = FibonacciLstSimple(test_list)
        self.assertEqual(fib_filter[0], 0, "Первый элемент должен быть 0")
        self.assertEqual(fib_filter[1], 1, "Второй элемент должен быть 1")
        self.assertEqual(fib_filter[2], 2, "Третий элемент должен быть 2")
        self.assertEqual(fib_filter[3], 5, "Четвёртый элемент должен быть 5")
        self.assertEqual(fib_filter[4], 8, "Пятый элемент должен быть 8")
        self.assertEqual(fib_filter[5], 13, "Шестой элемент должен быть 13")
        result = list(fib_filter)
        expected = [0, 1, 2, 5, 8, 13]
        self.assertEqual(result, expected, "Итерация должна вернуть все числа Фибоначчи")

if __name__ == '__main__':
    unittest.main(verbosity=2)