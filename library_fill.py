import uuid
import json

from faker import Faker

fake = Faker('ru-RU')

library_list = []  # Создание списка для хранения данных.

for i in range(10):  # Чем больше число - тем больше книг будет создано.
    # Создание словаря для хранения каждой отдельно взятой книги.
    book_dict = {
            'book_id': str(uuid.uuid4()),
            'title': fake.catch_phrase(),
            'author': fake.name(),
            'year': fake.year(),
            'status': 'В наличии'
    }

    # Добавление словаря с данными книги в список.
    library_list.append(book_dict)

with open('library.json', 'w', encoding='utf-8') as file:
    # Запись списка с данными книг в файл в формате JSON.
    json.dump(library_list, file, ensure_ascii=False, indent=4)
