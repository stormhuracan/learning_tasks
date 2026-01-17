import json
from enum import Enum

from debtor_class import DebtorInfo


# Используем перечисления, чтобы не ошибиться случайно
class BookStatuses(Enum):
    AVAILABLE = "available"
    ISSUED = "issued"
    LOST = "lost"


# Класс книги
class Book:
    def __init__(
        self,
        title,
        isbn,
        author,
        genre,
        year,
        status=None,
        id=None,
        owner: DebtorInfo | None = None,
    ):
        self.id = id
        self.title = title
        self.isbn = isbn
        self.author = author
        self.genre = genre
        self.year = year
        self.status = status or BookStatuses.AVAILABLE.value
        self.owner = owner

    @classmethod
    def from_dict(cls, **data):
        owner_data = data.get("owner")

        if owner_data is not None:
            data["owner"] = DebtorInfo.from_dict(owner_data)

        return cls(**data)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "isbn": self.isbn,
            "author": self.author,
            "genre": self.genre,
            "year": self.year,
            "status": self.status,
            "owner": self.owner.to_dict() if self.owner else None,
        }

    def __str__(self):
        return str(self.to_dict())


# Класс для работы с json`ом для книги
class DatabaseBookManager:

    # Загружает инфу о книгах из json`а
    @staticmethod
    def load_books(filename: str = "library.json") -> list[dict]:
        with open(filename, "r", encoding="utf-8") as file:
            try:
                return json.load(file)
            except json.decoder.JSONDecodeError:
                return []

    # Сохраняет список книг в json
    def save_books(self, books: list[Book], filename="library.json") -> bool:
        books = [book.to_dict() for book in books]
        with open(filename, "w", encoding="utf-8") as file:
            file.write(json.dumps(books, indent=4, ensure_ascii=False))
            return True


# Основной класс для работы с книгами
class BookManager:
    def __init__(self):
        self._db = DatabaseBookManager()
        books = self._db.load_books()  # Загружаем список книг в виде словаря
        self.list_books = [
            Book.from_dict(**dict_book) for dict_book in books
        ]  # Создаем экземпляры Book из списка books

    # Добавляет книгу
    def add_book(self, book: Book) -> bool:
        book.id = self._next_id()
        self.list_books.append(book)
        return True

    def remove_book(self, id_: int) -> bool:
        for book in self.list_books:
            if book.id == id_:
                self.list_books.remove(book)
                return True
        raise ValueError("Нет книги с таким ID!")

    def issue_book(self, book_name: str, debtor_info: DebtorInfo) -> bool | str:
        book_name = book_name.lower()
        if book_name not in (book.title.lower() for book in self.list_books):
            raise ValueError("У нас пока нет такой книги.")

        for book in self.list_books:
            if (
                book.title.lower() == book_name
                and book.status == BookStatuses.AVAILABLE.value
            ):
                book.status = BookStatuses.ISSUED.value
                book.owner = debtor_info
                return True
        raise ValueError(
            f'К сожалению, сейчас нет свободной книги "{book_name.capitalize()}",'
            f" приходите в следующий раз!"
        )

    def return_book(self, book_name: str, owner: DebtorInfo) -> bool | str:
        book_name = book_name.lower()
        if book_name not in (book.title.lower() for book in self.list_books):
            raise ValueError(f"У нас не было такой книги.")

        for book in self.list_books:
            if book.title.lower() == book_name and owner == book.owner:
                book.owner = None
                book.status = BookStatuses.AVAILABLE.value
                return True
        raise ValueError("Вы не должны нам такую книгу...")

    # Получить следующий id для книги
    def _next_id(self) -> int:
        if len(self.list_books) == 0:
            return 1
        return max(book.id for book in self.list_books) + 1

    def load(self):
        loaded_books = self._db.load_books()
        return loaded_books

    def save(self):
        self._db.save_books(self.list_books)
        return True
