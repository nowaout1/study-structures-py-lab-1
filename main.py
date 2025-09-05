import os
import sys
import random
import re
from datetime import date, timedelta
from typing import Callable, Self


MSG_GREETINGS: str = """
Задание 1 (вариант 2)
"""

MSG_MAIN_MENU: str = """
Введите номер упражнения, чтобы перейти к нему:
- Упражнение 1 (массивы)
- Упражнение 2 (строки)
- Упражнение 3 (односвязные списки)
"""

MSG_EXERCISE1: str = """
Введите номер варианта исполнения программы:
1. Ручной ввод чисел
2. Случайные числа
"""

MSG_EXERCISE2: str = """
Проверьте является ли введённая вами строка идентификатором
"""

MSG_EXERCISE3: str = """
Выберите действие с товарами:
1. Добавить товар
2. Отобразить весь список товаров
3. Искать товары
"""

MSG_EXERCISE3_VIEW_PRODUCTS: str = """
1. Сортировать по номеру склада
2. Сортировать по наименованию товара
3. Просроченные товары
"""

MSG_EXERCISE3_SEARCH_PRODUCTS: str = """
1. Поиск по наименованию товара
2. Поиск по номеру склада
"""

MSG_CONTINUE: str = """
Нажмите 'Enter', чтобы продолжить
"""

MSG_BACK: str = """
Введите 'q', чтобы вернуться назад
"""

MSG_QUIT: str = """
Введите 'q', чтобы выйти
"""

MSG_INPUT: str = "Ввод: "
MSG_INPUT_MANY_NUMBERS: str = "Введите числа через пробел: "
MSG_TRY_ENTER_AGAIN: str = "Попробуйте ещё раз"

MSG_ENTER_COUNT_OF_RANDOM_NUMBERS: str = "Введите количество случайных чисел: "
MSG_ENTER_LOWEST_OF_RANDOM_NUMBERS: str = "Введите минимальное среди случайных чисел: "
MSG_ENTER_HIGHEST_OF_RANDOM_NUMBERS: str = (
    "Введите максимальное среди случайных чисел: "
)

MSG_IT_IS_IDENTIFIER: str = "Введёная строка является идентификатором"
MSG_IT_IS_NOT_IDENTIFIER: str = "Введёная строка не является идентификатором"

MSG_ENTER_NAME: str = "Введите наименование: "
MSG_ENTER_WAREHOUSE_ID: str = "Введите номер склада: "
MSG_ENTER_DATE: str = "Введите дату поступления (в формате dd/mm/yy): "
MSG_ENTER_EXPIRES_IN: str = "Введите срок хранения в днях: "
MSG_ENTER_QUANTITY: str = "Введите количество единиц товара: "
MSG_ENTER_PRICE: str = "Введите цену за единицу товара: "

MSG_PRODUCT_SUCCESSFULLY_ADDED: str = "Товар успешно добавлен"


class Utils:
    @staticmethod
    def clear_terminal():
        """
        Вызывает команду очистки в терминале в зависимости от платформы:
        `cls` - windows
        `clear` - linux
        """

        os.system("cls" if os.name == "nt" else "clear")


class InputExt:
    @staticmethod
    def press_enter():
        input(MSG_CONTINUE)

    @staticmethod
    def string(label: str = "") -> str:
        return input(label)

    @staticmethod
    def int(label: str = "") -> int:
        while True:
            try:
                return int(input(label))
            except:
                print(MSG_TRY_ENTER_AGAIN)

    @staticmethod
    def float(label: str = "") -> float:
        while True:
            try:
                return float(input(label))
            except:
                print(MSG_TRY_ENTER_AGAIN)

    @staticmethod
    def date(label: str = "") -> date:
        """
        Считывает строку как дату в формате dd/mm/yy
        """

        while True:
            try:
                [day, month, year] = [int(x) for x in input(label).split("/")]

                # Если год указан сокращённо, то указать полный его формат.
                # Пример: 25 -> 2025 (год)
                if year < 100:
                    year += 2000

                return date(day=day, month=month, year=year)
            except:
                print(MSG_TRY_ENTER_AGAIN)

    @staticmethod
    def many_floats(label: str = "", sep: str = " "):
        """
        Запрашивает ввод чисел от пользователя через пробел
        и собирает полученную строку в массив чисел,
        иначе снова запрашивает ввод.

        `label` (необязательный)
            Сообщение пользователю

        `sep` (необязательный)
            Разделитель между числами (по умолчанию пробел)
        """

        while True:
            try:
                maybe_nums: str = input(label)
                return [float(x) for x in maybe_nums.split(sep)]
            except:
                print(MSG_TRY_ENTER_AGAIN)

    @staticmethod
    def choice(menu: dict[str, list[Callable]], label: str = ""):
        """
        Выполняет команды из меню, выбранные пользователем.

        `menu`
            Набор команд, где:
            Ключи - названия команд, которые требуется ввести пользователю
            Значения - последовательность выполняемых функций

        `label` (необязательный)
            Сообщение пользователю

        Пример:
        ```python
        InputExt.choice(
            label="Введите команду",
            variants={
                "run": [greetings, menu]
                "exit": [exit],
            }
        )
        ```
        """

        try:
            # Название выбранной команды
            chosen = input(label)

            # Выборка исполняемых команд, если не существует вернёт ошибку (`KeyError`)
            commands = menu[chosen]

            # Исполнение команд
            for execute in commands:
                execute()

        except KeyError:
            pass


class Product:
    def __init__(
        self,
        warehouse_id: int,  # номер склада
        name: str,  # наименование товара
        quantity: int,  # количество единиц товара
        price: float,  # цена за единицу товара
        date: date,  # дата поступления на склад
        expires_in: timedelta,  # срок хранения в днях
        id: int = random.randint(0, 999_999),  # код товара
    ):
        self.id = id
        self.warehouse_id = warehouse_id
        self.name = name
        self.quantity = quantity
        self.price = price
        self.date = date
        self.expires_in = expires_in


class LinkedProduct:
    COL_WIDTH: int = 16
    SEPARATOR: str = " | "
    HEADERS: str = SEPARATOR.join(
        [
            f"{'Товар':<{COL_WIDTH}}",
            f"{'Код товара':<{COL_WIDTH}}",
            f"{'Номер склада':<{COL_WIDTH}}",
            f"{'Количество':<{COL_WIDTH}}",
            f"{'Цена (шт.)':<{COL_WIDTH}}",
            f"{'Дата поступления':<{COL_WIDTH}}",
            f"{'Срок хранения':<{COL_WIDTH}}",
        ]
    )

    def __init__(self, product: Product | None = None, next: Self | None = None):
        self.product: Product | None = product
        self.next: Self | None = next

    @staticmethod
    def from_array(products: list[Product]):
        lp = LinkedProduct()

        for p in reversed(products):
            lp = LinkedProduct(p, next=lp)

        return lp

    def __str__(self) -> str:
        def format_product(p: Product) -> str:
            date_expires_in = p.date + p.expires_in

            return LinkedProduct.SEPARATOR.join(
                [
                    f"{p.name:<{LinkedProduct.COL_WIDTH}}",
                    f"{p.id:<{LinkedProduct.COL_WIDTH}}",
                    f"{p.warehouse_id:<{LinkedProduct.COL_WIDTH}}",
                    f"{p.quantity:<{LinkedProduct.COL_WIDTH}}",
                    f"{p.price:<{LinkedProduct.COL_WIDTH}}",
                    f"{p.date.strftime('%d.%m.%Y'):<{LinkedProduct.COL_WIDTH}}",
                    f"{date_expires_in.strftime('%d.%m.%Y'):<{LinkedProduct.COL_WIDTH}}",
                ]
            )

        delimiter = "-" * len(LinkedProduct.HEADERS)
        products = "\n".join(format_product(p) for p in self.all)

        return LinkedProduct.HEADERS + "\n" + delimiter + "\n" + products

    @property
    def is_product_empty(self) -> bool:
        return self.product is None

    @property
    def all(self) -> list[Product]:
        """
        Геттер, преобразующий односвязный список товаров
        в массив товаров и возвращающий его.
        """

        current: LinkedProduct | None = self
        products: list[Product] = []

        while current is not None and current.product is not None:
            products.append(current.product)
            current = current.next

        return products

    def sorted_by_warehouse_id(self, reverse=False):
        key = lambda product: product.warehouse_id
        products = sorted(self.all, key=key, reverse=reverse)

        return LinkedProduct.from_array(products)

    def sorted_by_name(self, reverse=False):
        key = lambda product: product.name.lower()
        products = sorted(self.all, key=key, reverse=reverse)

        return LinkedProduct.from_array(products)

    @staticmethod
    def filter_by_warehouse_id(products: list[Product], warehouse_id: int):
        """
        Поиск товаров по ID склада.
        """

        return LinkedProduct.from_array(
            [p for p in products if p.warehouse_id == warehouse_id]
        )

    @staticmethod
    def filter_by_product_name(products: list[Product], name: str):
        """
        Поиск товаров по имени.
        """

        return LinkedProduct.from_array(
            [p for p in products if name.lower() in p.name.lower()]
        )

    def get_expired_products(self):
        """
        Возвращает список просроченных товаров.
        """

        now = date.today()
        return LinkedProduct.from_array(
            [p for p in self.all if p.date + p.expires_in < now]
        )


class Program:
    def __init__(self):
        self.is_running: bool = True

    def stop(self):
        self.is_running = False


class Exercise1(Program):
    """
    Упражнение 1 (вариант 2)

    Дан одномерный целочисленный массив порядка N.
    Найдите сумму отрицательных элементов массива.
    Если таких элементов нет, вернуть значение 0.
    """

    def __init__(self):
        super().__init__()
        self.nums: list[float] = []  # Буфер для чисел

    def run(self):
        while self.is_running:
            Utils.clear_terminal()

            print(MSG_EXERCISE1)
            print(MSG_BACK)

            InputExt.choice(
                menu={
                    "q": [self.stop],
                    "1": [
                        self.manually,
                        self.sum_of_negatives,
                        InputExt.press_enter,
                        self.stop,
                    ],
                    "2": [
                        self.automatically,
                        self.sum_of_negatives,
                        InputExt.press_enter,
                        self.stop,
                    ],
                },
                label=MSG_INPUT,
            )

    def manually(self):
        """
        Запрашивает ручной ввод чисел от пользователя
        """

        self.nums = InputExt.many_floats(label=MSG_INPUT_MANY_NUMBERS)

    def automatically(self):
        """
        Генерирует случайные числа на основе заданных пользователем параметров
        """

        count: int = InputExt.int(MSG_ENTER_COUNT_OF_RANDOM_NUMBERS)
        low: int = InputExt.int(MSG_ENTER_LOWEST_OF_RANDOM_NUMBERS)
        high: int = InputExt.int(MSG_ENTER_HIGHEST_OF_RANDOM_NUMBERS)

        self.nums = [random.randint(low, high) for _ in range(count)]

    def sum_of_negatives(self):
        """
        Вычисляет сумму отрицательных чисел и выводит её
        """

        negatives = [x for x in self.nums if x < 0]

        print("Дан массив:", self.nums)
        print("Сумма отрицательных чисел:", sum(negatives))


class Exercise2(Program):
    """
    Упражнение 2 (вариант 2)

    Является ли строка идентификатором
    Определить, является ли введенное слово идентификатором,
    т.е. начинается ли оно с английской буквы в любом регистре
    или знака подчеркивания и не содержит других символов,
    кроме букв английского алфавита (в любом регистре), цифр и знака подчеркивания.
    """

    IDENTIFIER_PATTERN: re.Pattern[str] = re.compile(
        r"([a-zA-Z_])([a-zA-Z0-9_])*", re.VERBOSE
    )

    def run(self):
        Utils.clear_terminal()

        print(MSG_EXERCISE2)
        user_input = input(MSG_INPUT)

        match self.is_identifier(user_input):
            case True:
                print(MSG_IT_IS_IDENTIFIER)
            case False:
                print(MSG_IT_IS_NOT_IDENTIFIER)

        InputExt.press_enter()

    def is_identifier(self, value: str) -> bool:
        """
        Проверяет первую букву на наличие:
        - Английских букв без учёта регистра
        - Символа нижнего подчёркивания

        Проверяет наличие:
        - Английских букв без учёта регистра
        - Арабских цифр
        - Символов подчёркивания
        """

        return bool(re.fullmatch(Exercise2.IDENTIFIER_PATTERN, value))


class Exercise3(Program):
    """
    Упражнение 3 (вариант 2)

    Запись о товаре на складе представляет собой структуру с полями:
    - номер склада
    - код товара
    - наименование товара
    - дата поступления на склад
    - срок хранения в днях
    - количество единиц товара
    - цена за единицу товара.
    Поиск и сортировка — по номеру склада, наименованию товара.
    Вывести список простроченных товаров
    (поиск всех товаров, у которых на текущую дату истек срок хранения).
    """

    MOCK_PRODUCTS: LinkedProduct = LinkedProduct(
        Product(
            id=186125,
            warehouse_id=131,
            name="Горшок цветочный",
            quantity=511,
            price=7.99,
            date=date(year=2025, month=7, day=14),
            expires_in=timedelta(days=14),
        ),
        next=LinkedProduct(
            Product(
                id=51259,
                warehouse_id=743,
                name="Авокадо",
                quantity=146,
                price=2.99,
                date=date(year=2025, month=9, day=7),
                expires_in=timedelta(days=7),
            )
        ),
    )

    def __init__(self, products: LinkedProduct = MOCK_PRODUCTS):
        super().__init__()
        self.products: LinkedProduct = products

    def run(self):
        while self.is_running:
            Utils.clear_terminal()

            print(MSG_EXERCISE3)
            print(MSG_BACK)

            InputExt.choice(
                menu={
                    "q": [self.stop],
                    "1": [self.add_product],
                    "2": [self.view_products],
                    "3": [self.search_products],
                },
                label=MSG_INPUT,
            )

    def add_product(self):
        Utils.clear_terminal()

        name = InputExt.string(MSG_ENTER_NAME)
        warehouse_id = InputExt.int(MSG_ENTER_WAREHOUSE_ID)
        date = InputExt.date(MSG_ENTER_DATE)
        expires_in = timedelta(days=InputExt.int(MSG_ENTER_EXPIRES_IN))
        quantity = InputExt.int(MSG_ENTER_QUANTITY)
        price = InputExt.float(MSG_ENTER_PRICE)

        self.products = LinkedProduct(
            Product(
                name=name,
                warehouse_id=warehouse_id,
                date=date,
                expires_in=expires_in,
                quantity=quantity,
                price=price,
            ),
            next=self.products,
        )

        print(MSG_PRODUCT_SUCCESSFULLY_ADDED)

        InputExt.press_enter()

    def view_products(self):
        Utils.clear_terminal()

        print(MSG_EXERCISE3_VIEW_PRODUCTS)
        print(MSG_BACK)

        InputExt.choice(
            menu={
                "1": [
                    self.view_products_sorted_by_warehouse_id,
                ],
                "2": [
                    self.view_products_sorted_by_name,
                ],
                "3": [
                    self.view_expired_products,
                ],
            },
            label=MSG_INPUT,
        )

    def view_products_sorted_by_warehouse_id(self):
        Utils.clear_terminal()

        print(self.products.sorted_by_warehouse_id())

        InputExt.press_enter()

    def view_products_sorted_by_name(self):
        Utils.clear_terminal()

        print(self.products.sorted_by_name())

        InputExt.press_enter()

    def view_expired_products(self):
        Utils.clear_terminal()

        print(self.products.get_expired_products())

        InputExt.press_enter()

    def search_products(self):
        Utils.clear_terminal()

        print(MSG_EXERCISE3_SEARCH_PRODUCTS)
        print(MSG_BACK)

        InputExt.choice(
            menu={"1": [self.search_by_name], "2": [self.search_by_warehouse_id]},
            label=MSG_INPUT,
        )

    def search_by_name(self):
        Utils.clear_terminal()

        name = InputExt.string(MSG_ENTER_NAME)
        products = LinkedProduct.filter_by_product_name(
            products=self.products.all, name=name
        )

        match products.is_product_empty:
            case True:
                print("Ничего не найдено")
            case False:
                print(products)

        InputExt.press_enter()

    def search_by_warehouse_id(self):
        Utils.clear_terminal()

        warehouse_id = InputExt.int(MSG_ENTER_WAREHOUSE_ID)
        products = LinkedProduct.filter_by_warehouse_id(
            products=self.products.all, warehouse_id=warehouse_id
        )

        match products.is_product_empty:
            case True:
                print("Ничего не найдено")
            case False:
                print(products)

        InputExt.press_enter()


def main():
    while True:
        Utils.clear_terminal()

        print(MSG_GREETINGS)
        print(MSG_MAIN_MENU)
        print(MSG_QUIT)

        InputExt.choice(
            menu={
                "q": [sys.exit],
                "1": [Exercise1().run],
                "2": [Exercise2().run],
                "3": [Exercise3().run],
            },
            label=MSG_INPUT,
        )


if __name__ == "__main__":
    main()
