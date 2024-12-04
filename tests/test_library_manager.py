import json
from io import StringIO
import os

import pytest

from library_manage import Library, Book

sample_books = [
    {
        "book_id": "83d80f3f-874e-4150-91ed-aa7986b5f7cd",
        "title": "Органичная и направленная координация",
        "author": "Архип Георгиевич Беляков",
        "year": "1979",
        "status": "В наличии"
    },
    {
        "book_id": "1eea1a99-410a-4524-b374-b2c9f1b04a16",
        "title": "Автоматизированное и специализированное ядро",
        "author": "Моисеев Селиверст Артурович",
        "year": "1973",
        "status": "В наличии"
    },
    {
        "book_id": "9acfe847-1910-4d20-b0f4-b8fbb384b942",
        "title": "Амортизированное и направленное оборудование",
        "author": "Волкова Антонина Антоновна",
        "year": "1990",
        "status": "В наличии"
    }
]


@pytest.fixture
def sample_library():
    library = Library("test_books.json")
    library.books = [Book(**book) for book in json.load(StringIO(json.dumps(sample_books, ensure_ascii=False)))]
    return library


# Тест успешной загрузки книг
def test_load_books_success(monkeypatch):
    library = Library()  # Создаем экземпляр библиотеки

    # Определяем функцию mock_open, которая будет возвращать StringIO объект
    def mock_open():
        return StringIO(json.dumps(sample_books, ensure_ascii=False))

    monkeypatch.setattr('builtins.open', lambda *args, **kwargs: mock_open())  # Используем monkeypatch для замены функции open на mock_open
    books = library.load_books()  # Вызываем функцию load_books

    # Проверяем, что данные книг были загружены
    assert len(books) == 3
    assert books[0].title == "Органичная и направленная координация"
    assert books[1].author == "Моисеев Селиверст Артурович"
    assert books[2].year == "1990"


# Тест обработки отсутствующего файла
def test_load_books_file_not_found(monkeypatch):
    library = Library()  # Создаем экземпляр библиотеки

    # Определяем функцию mock_open, которая будет вызывать ошибку FileNotFoundError
    def mock_open():
        raise FileNotFoundError

    monkeypatch.setattr('builtins.open', lambda *args, **kwargs: mock_open())  # Используем monkeypatch для замены функции open на mock_open
    books = library.load_books()  # Вызываем функцию load_books
    assert books == []  # Проверяем, что библиотека пуста


# Тест успешного сохранения книг
def test_save_books_success(monkeypatch, sample_library):
    # Определяем функцию mock_open, которая будет возвращать StringIO объект
    def mock_open():
        return StringIO(json.dumps(sample_books, ensure_ascii=False))

    monkeypatch.setattr('builtins.open', lambda *args, **kwargs: mock_open())  # Используем monkeypatch для замены функции open на mock_open
    sample_library.save_books()  # Вызываем функцию save_books

    # Проверяем, что данные книг были записаны в файл в формате JSON
    with open("test_books.json", 'r', encoding='utf-8') as file:
        books = json.load(file)
        assert len(books) == 3
        assert books[0]['title'] == "Органичная и направленная координация"
        assert books[1]['author'] == "Моисеев Селиверст Артурович"
        assert books[2]['year'] == "1990"


# Тест обработки ошибки при записи в файл
def test_save_books_io_error(monkeypatch, sample_library):
    # Определяем функцию mock_open, которая будет вызывать IOError
    def mock_open():
        raise IOError("Unable to write to file")

    monkeypatch.setattr('builtins.open', lambda *args, **kwargs: mock_open())  # Используем monkeypatch для замены функции open на mock_open

    # Проверяем, что при вызове save_books возникает IOError
    with pytest.raises(IOError, match="Unable to write to file"):
        sample_library.save_books()


# Тест успешного добавления книги
def test_add_book(monkeypatch):
    library = Library("test_books.json")  # Создаем экземпляр библиотеки

    # Определяем функцию mock_save_books, которая ничего не делает
    def mock_save_books():
        pass

    monkeypatch.setattr(library, "save_books", mock_save_books)  # Используем monkeypatch для замены метода save_books на mock_save_books
    library.add_book(3, "Book 3", "Author 3", 2023)  # Добавляем книгу

    # Проверяем, что книга добавлена в список книг
    assert len(library.books) == 1
    assert library.books[0].book_id == 3
    assert library.books[0].title == "Book 3"
    assert library.books[0].author == "Author 3"
    assert library.books[0].year == 2023
    assert library.books[0].status == "В наличии"


# Тест добавления книги с проверкой сохранения
def test_add_book_with_save(monkeypatch):
    library = Library("test_books.json")  # Создаем экземпляр библиотеки

    # Определяем функцию mock_save_books, которая проверяет вызов сохранения
    def mock_save_books():
        library.save_called = True

    monkeypatch.setattr(library, "save_books", mock_save_books)  # Используем monkeypatch для замены метода save_books на mock_save_books
    library.add_book(4, "Book 4", "Author 4", 2024)  # Добавляем книгу

    # Проверяем, что книга добавлена в список книг и сохранение вызвано
    assert len(library.books) == 1
    assert library.books[0].book_id == 4
    assert library.books[0].title == "Book 4"
    assert library.books[0].author == "Author 4"
    assert library.books[0].year == 2024
    assert library.books[0].status == "В наличии"
    assert library.save_called


# Тест успешного удаления книги
def test_remove_book_success(monkeypatch, sample_library):
    # Определяем функцию mock_save_books, которая ничего не делает
    def mock_save_books():
        pass

    monkeypatch.setattr(sample_library, "save_books", mock_save_books)  # Используем monkeypatch для замены метода save_books на mock_save_books
    sample_library.remove_book('83d80f3f-874e-4150-91ed-aa7986b5f7cd')  # Удаляем книгу с ID

    # Проверяем, что книга удалена из списка книг
    assert len(sample_library.books) == 2
    assert sample_library.books[0].book_id == '1eea1a99-410a-4524-b374-b2c9f1b04a16'


# Тест удаления книги, которая не существует
def test_remove_book_not_found(monkeypatch, capsys, sample_library):
    # Определяем функцию mock_save_books, которая ничего не делает
    def mock_save_books():
        pass

    monkeypatch.setattr(sample_library, "save_books", mock_save_books)  # Используем monkeypatch для замены метода save_books на mock_save_books
    sample_library.remove_book('3')  # Пытаемся удалить книгу с несуществующим ID

    assert len(sample_library.books) == 3  # Проверяем, что список книг не изменился

    # Проверяем, что выводится сообщение об ошибке
    captured = capsys.readouterr()
    assert "Книга с ID 3 не найдена" in captured.out


def test_find_book_by_title(monkeypatch, sample_library):
    # Тестирование поиска книги по названию.
    inputs = iter(['1', 'Органичная и направленная координация'])  # Список воода пользователя
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))  # Используем monkeypatch для замены ввода на '1' и на 'Органичная и направленная координация'
    results = sample_library.find_book()  # Вызываем функцию find_book

    assert len(results) == 1  # Проверка, что найдена одна книга.
    assert results[0].title == "Органичная и направленная координация"  # Проверка, что название найденной книги 'Органичная и направленная координация'


def test_find_book_by_author(monkeypatch, sample_library):
    # Тестирование поиска книги по автору.
    inputs = iter(['2', 'Моисеев Селиверст Артурович'])  # Список воода пользователя
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))  # Используем monkeypatch для замены ввода на '2' и на 'Моисеев Селиверст Артурович'
    results = sample_library.find_book()  # Вызываем функцию find_book

    assert len(results) == 1  # Проверка, что найдена одна книга.
    assert results[0].author == "Моисеев Селиверст Артурович"  # Проверка, что автор найденной книги 'Моисеев Селиверст Артурович'.


def test_find_book_by_year(monkeypatch, sample_library):
    # Тестирование поиска книги по году издания.
    inputs = iter(['3', '1990'])  # Список воода пользователя
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))  # Используем monkeypatch для замены ввода на '3' и на '1990'
    results = sample_library.find_book()  # Вызываем функцию find_book

    assert len(results) == 1  # Проверка, что найдена одна книга.
    assert results[0].year == "1990"  # Проверка, что год издания найденной книги '1990'.


def test_display_books_with_books(capsys, sample_library):
    # Тестирование отображения книг, когда книги есть в библиотеке.
    table = sample_library.display_books()  # Вызываем функцию display_books
    captured = capsys.readouterr()

    assert "Список всех книг библиотеки:" in captured.out  # Проверка, что выводится заголовок списка книг.
    assert len(table.rows) == 3  # Проверка, что в таблице 3 строки (3 книги).

    # Проверка содержимого таблицы
    expected_rows = [
        ["83d80f3f-874e-4150-91ed-aa7986b5f7cd", "Органичная и направленная координация", "Архип Георгиевич Беляков",
         "1979", "В наличии"],
        ["1eea1a99-410a-4524-b374-b2c9f1b04a16", "Автоматизированное и специализированное ядро",
         "Моисеев Селиверст Артурович", "1973", "В наличии"],
        ["9acfe847-1910-4d20-b0f4-b8fbb384b942", "Амортизированное и направленное оборудование",
         "Волкова Антонина Антоновна", "1990", "В наличии"]
    ]

    for row in expected_rows:
        assert row in table.rows  # Проверка, что каждая ожидаемая строка присутствует в таблице.


def test_display_books_no_books(capsys):
    # Тестирование отображения, когда книг нет в библиотеке.
    empty_library = Library()  # Создание экземпляра пустой библиотеки
    empty_library.books = []
    empty_library.display_books()  # Вызываем функцию display_books
    captured = capsys.readouterr()

    assert "Библиотека не найдена." in captured.out  # Проверка, что выводится сообщение об отсутствии книг.


def test_update_status_success(capsys, sample_library):
    # Тестирование успешного обновления статуса книги.
    sample_library.update_status("83d80f3f-874e-4150-91ed-aa7986b5f7cd", "Выдана")  # Вызываем функцию update_status
    captured = capsys.readouterr()

    assert "Статус книги с ID 83d80f3f-874e-4150-91ed-aa7986b5f7cd обновлен на 'Выдана'" in captured.out  # Проверка, что выводится сообщение об обновлении статуса.
    assert sample_library.books[0].status == "Выдана"  # Проверка, что статус книги обновлен.


def test_update_status_same_status(capsys, sample_library):
    # Тестирование попытки обновления статуса на тот же самый.
    sample_library.update_status("1eea1a99-410a-4524-b374-b2c9f1b04a16", "В наличии")  # Вызываем функцию update_status
    captured = capsys.readouterr()

    assert "Статус книги с ID 1eea1a99-410a-4524-b374-b2c9f1b04a16 уже соответствует статусу 'В наличии'" in captured.out  # Проверка, что выводится сообщение о том, что статус уже соответствует.
    assert sample_library.books[0].status == "В наличии"  # Проверка, что статус книги не изменился.


def test_update_status_book_not_found(capsys, sample_library):
    # Тестирование попытки обновления статуса книги, которой нет в библиотеке.
    sample_library.update_status("777", "Выдана")  # Вызываем функцию update_status
    captured = capsys.readouterr()

    assert "Книга с ID 777 не найдена" in captured.out  # Проверка, что выводится сообщение об ошибке.

    os.remove("test_books.json")  # Удаление тестового JSON файла библиотеки
