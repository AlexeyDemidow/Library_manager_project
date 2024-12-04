import json
import uuid

from prettytable import PrettyTable


class Book:
    """
        Класс Book представляет книгу с уникальным идентификатором, названием, автором, годом издания и статусом.
    """
    def __init__(self, book_id, title, author, year, status="В наличии"):
        self.book_id = book_id  # Уникальный идентификатор для каждой книги.
        self.title = title  # Название книги.
        self.author = author  # Автор книги.
        self.year = year  # Год издания книги.
        self.status = status  # Статус книги (по умолчанию "В наличии").


class Library:
    """
        Класс Library представляет библиотеку, которая управляет коллекцией книг.
    """
    def __init__(self, filename='library.json'):
        self.filename = filename  # Имя файла для хранения данных библиотеки.
        self.books = self.load_books()  # Загрузка книг из файла при инициализации библиотеки.

    # Метод для загрузки книг из файла.
    def load_books(self):
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                # Чтение данных из файла и создание объектов Book.
                return [Book(**book) for book in json.load(file)]
        except FileNotFoundError:
            # Если файл не найден, возвращаем пустой список.
            return []

    # Метод для сохранения книг в файл.
    def save_books(self):
        with open(self.filename, 'w', encoding='utf-8') as file:
            # Запись данных книг в файл в формате JSON.
            json.dump([book.__dict__ for book in self.books], file, ensure_ascii=False, indent=4)

    # Метод для добавления новой книги в библиотеку.
    def add_book(self, book_id, title, author, year, status="В наличии"):
        book = Book(book_id, title, author, year, status)  # Создание нового объекта Book.
        self.books.append(book)  # Добавление книги в список книг.
        self.save_books()  # Сохранение обновленного списка книг в файл.
        print(f"\nКнига '{title}' добавлена с ID {book.book_id}\n")

    # Метод для удаления книги из библиотеки по ID.
    def remove_book(self, book_id):
        if any(book.book_id == book_id for book in self.books):
            # Если книга с указанным ID существует, удаляем её.
            self.books = [book for book in self.books if book.book_id != book_id]
            self.save_books()  # Сохранение обновленного списка книг в файл.
            print(f"Книга с ID {book_id} удалена\n")
        else:
            # Если книга с указанным ID не найдена, выводим сообщение об ошибке.
            print(f"\nКнига с ID {book_id} не найдена\n")

    # Метод для поиска книг по названию или автору.
    def find_book(self):
        # Поиск книг, содержащих поисковый запрос в названии или имени автора.
        print('\nКак произвести поиск?')
        print('1. По названию.')
        print('2. По имени автора.')
        print('3. По году издания.')

        choice = input('\nВыберите действие:\n')
        results = []

        if choice == '1':
            search_term = input('\nВведите название книги.\n')
            results = [book for book in self.books if search_term.lower() in book.title.lower()]
        elif choice == '2':
            search_term = input('\nВведите автора книги.\n')
            results = [book for book in self.books if search_term.lower() in book.author.lower()]
        elif choice == '3':
            search_term = input('\nВведите год издания.\n')
            results = [book for book in self.books if search_term.lower() in book.year]

        return results

    # Метод для отображения всех книг в библиотеке.
    def display_books(self):
        if not self.books:
            # Если файла библиотеки нет, то будет отображено сообщение об ошибке
            print('\nБиблиотека не найдена.')
        else:
            print('\nСписок всех книг библиотеки:')
            all_books_table = PrettyTable()  # Используем библиотеку prettytable для красивого отображения библиотеки в виде таблицы
            all_books_table.field_names = ["ID", "Название книги", "Автор", "Год издания", "Статус"]  # Имена полей таблицы
            for book in self.books:
                # Добавление информации о каждой книге в таблицу.
                all_books_table.add_row([book.book_id, book.title, book.author, book.year, book.status])
            return all_books_table  # Вывод таблицы в терминал.

    # Метод для обновления статуса книги по ID.
    def update_status(self, book_id, new_status):
        for book in self.books:
            if book.book_id == book_id:
                # Если книга с указанным ID найдена - обновляем её статус.
                if book.status != new_status:
                    book.status = new_status
                    print(f"\nСтатус книги с ID {book_id} обновлен на '{new_status}'\n")
                else:
                    # Если книга с указанным ID не найдена - выводим соответствующее сообщение.
                    print(f"\nСтатус книги с ID {book_id} уже соответствует статусу '{new_status}'\n")
                self.save_books()  # Сохранение обновленного списка книг в файл.
                return
        # Если книга с указанным ID не найдена, выводим сообщение об ошибке.
        print(f"Книга с ID {book_id} не найдена")


# Основная функция для работы с библиотекой через консоль.
def main():
    library = Library()  # Создание объекта библиотеки.
    while True:
        # Вывод меню для выбора действия.
        print('*' * 100)
        print('Добро пожаловать в приложение управления библиотекой. Выберите нужный пункт в меню.')
        print("\n1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Найти книгу")
        print("4. Показать все книги")
        print("5. Изменить статус книги")
        print("6. Выйти")
        print('*' * 100)
        choice = input("\nВыберите действие:\n")

        if choice == '1':
            # Добавление новой книги.
            book_id = str(uuid.uuid4())
            title = input("\nВведите название книги:\n")
            author = input("\nВведите автора книги:\n")
            year = input("\nВведите год издания книги:\n")
            library.add_book(book_id, title, author, year)
        elif choice == '2':
            # Удаление книги по ID.
            book_id = input("\nВведите ID книги для удаления:\n")
            library.remove_book(book_id)
        elif choice == '3':
            # Поиск книги по названию, автору или году издания.
            results = library.find_book()
            if results:
                search_result_table = PrettyTable()
                search_result_table.field_names = ["ID", "Название книги", "Автор", "Год издания", "Статус"]
                print('\nРезультаты поиска:')
                for book in results:
                    search_result_table.add_row([book.book_id, book.title, book.author, book.year, book.status])
                # Выводим результаты поиска в виде таблицы
                print(search_result_table)
            else:
                print("Книги не найдены")
        elif choice == '4':
            # Отображение всех книг.
            print(library.display_books())
        elif choice == '5':
            # Изменение статуса книги по ID.
            book_id = input("Введите ID книги для изменения статуса:\n")
            status_choice = input("Введите новый статус (1. В наличии/2. Выдана):\n")
            new_status = ''
            if status_choice == '1':
                new_status = 'В наличии'
            elif status_choice == '2':
                new_status = 'Выдана'
            library.update_status(book_id, new_status)
        elif choice == '6':
            library.save_books()
            # Выход из программы.
            break
        else:
            # Обработка неверного выбора.
            print("Неверный выбор, попробуйте снова")


if __name__ == "__main__":
    main()
