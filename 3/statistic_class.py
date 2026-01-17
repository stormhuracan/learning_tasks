from book_class import Book, DatabaseBookManager


class LibraryStatistics:
    def __init__(self, library="library.json"):
        books = DatabaseBookManager.load_books(library)
        self.library = [Book.from_dict(**book) for book in books]

    def books_by_condition(self, condition: str) -> dict[str | int, int]:
        result = {}
        for book in self.library:
            value = getattr(book, condition, None)
            if value is None:
                continue
            result[value] = result.get(value, 0) + 1
        return result

    def taken_books_by_condition(self, condition: str) -> dict[str | int, int]:
        """
        Считает только книги, которые выданы (owner != None),
        группируя их по любому атрибуту: genre, year, author и т.д.
        """
        result = {}
        for book in self.library:
            if book.owner is None:
                continue  # пропускаем свободные книги
            value = getattr(book, condition, None)
            if value is None:
                continue
            result[value] = result.get(value, 0) + 1
        return result

    def get_statistics(self):
        return (
            f"Кол-во книг по жанрам: {self.books_by_condition('genre')}\n"
            f"Кол-во книг по годам: {self.books_by_condition('year')}\n"
            f"Книги, которые взяты читателями по жанру: {self.taken_books_by_condition('genre')}\n"
        )


x = LibraryStatistics()
print(x.get_statistics())
