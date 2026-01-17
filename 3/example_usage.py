from book_class import Book, BookManager
from debtor_class import DebtorInfo
from statistic_class import LibraryStatistics


def main():
    # --- Создаем менеджер библиотеки ---
    manager = BookManager()

    # --- Добавляем книги (если библиотеки пусты) ---
    if len(manager.list_books) == 0:
        books_to_add = [
            Book("Над пропастью во ржи", "ISBN-001", "Дж. Сэлинджер", "fiction", 1951),
            Book("1984", "ISBN-002", "Дж. Оруэлл", "fiction", 1949),
            Book("Мастер и Маргарита", "ISBN-003", "М. Булгаков", "fiction", 1967),
            Book("Clean Code", "ISBN-004", "R. Martin", "programming", 2008),
            Book("Python Tricks", "ISBN-005", "D. Bader", "programming", 2017),
            Book("Анна Каренина", "ISBN-006", "Л. Толстой", "fiction", 1877),
        ]
        for book in books_to_add:
            manager.add_book(book)
        manager.save()
        print("Библиотека заполнена начальными книгами.\n")

    # --- Создаем пользователей ---
    vasya = DebtorInfo("Вася", "+79990000001")
    lesha = DebtorInfo("Лёша", "+79990000002")

    # --- Выдача книг ---
    print("Выдача книг:")
    try:
        print(
            "Над пропастью во ржи -> Вася:",
            manager.issue_book("Над пропастью во ржи", vasya),
        )
        print("Анна Каренина -> Лёша:", manager.issue_book("Анна Каренина", lesha))
        print("1984 -> Вася:", manager.issue_book("1984", vasya))
    except Exception as e:
        print("Ошибка при выдаче книги:", e)
    print()

    # --- Возврат книг с обработкой исключений ---
    print("Возврат книг:")
    try:
        res = manager.return_book("Над пропастью во ржи", vasya)
        print("Возврат 'Над пропастью во ржи' Вася:", res)
    except Exception as e:
        print("Ошибка при возврате книги:", e)

    try:
        # Попытка вернуть чужую книгу
        res = manager.return_book("Clean Code", vasya)
        print("Возврат 'Clean Code' Вася:", res)
    except Exception as e:
        print("Ошибка при возврате книги:", e)
    print()

    # --- Сохраняем изменения ---
    manager.save()

    # --- Текущее состояние библиотеки ---
    print("Текущее состояние библиотеки:")
    for book in manager.list_books:
        print(book)
    print()

    # --- Статистика ---
    stats = LibraryStatistics()
    print("Статистика всех книг:")
    print(stats.get_statistics())

    print("Статистика только выданных книг по жанру:")
    print(stats.taken_books_by_condition("genre"))

    print("Статистика только выданных книг по году:")
    print(stats.taken_books_by_condition("year"))


if __name__ == "__main__":
    main()
