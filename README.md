# Система управления библиотекой

---
Консольная система управления библиотекой книг с возможностью добавлять, удалять, искать и отображать книги.
<br>

Каждая книга должна содержать следующие поля:
- `book_id` (уникальный идентификатор, генерируется автоматически)
- `title` (название книги)
- `author` (автор книги)
- `year` (год издания)
- `status` (статус книги: “в наличии”, “выдана”)


## Функционал

---
 1. Добавление книги: Пользователь вводит `title`, author и year, после чего книга добавляется в библиотеку с уникальным id и статусом “в наличии”.
 2. Удаление книги: Пользователь вводит `book_id` книги, которую нужно удалить.
 3. Поиск книги: Пользователь может искать книги по `title`, `author` или `year`.
 4. Отображение всех книг: Приложение выводит список всех книг с их `book_id`, `title`, `author`, `year` и `status`.
 5. Изменение статуса книги: Пользователь вводит `book_id` книги и новый статус (“В наличии” или “Выдана”).

## Установка и запуск

---

- Выполнить команду `git clone https://github.com/AlexeyDemidow/Library_manager_project.git`.
- Выполнить команду `pip install -r requirements.txt`.
- Для создания файла библиотеки и заполнения его данными выполнить файл `library_fill.py` выполнив команду `python library_fill.py`.
- Для запуска консольной системы управления библиотекой выполнить файл `library_manage.py` выполнив команду `python libary_manage.py`
- Для запуска тестов выполнить команду `pytest`. Для большей наглядности можно добавить флаг `-v`
Тесты находятся в папке `tests`.

## Используемые технологии

---

- `Python 3.12.3`
- `Faker 33.1.0` для заполнения данными фала библиотеки.
- `prettytable 3.12.0` для удобного вывода данных в консоль.
- `pytest 8.3.4` для тестирования приложения.
