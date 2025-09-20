from __future__ import annotations
from dataclasses import dataclass
from typing import List, Protocol, Callable
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


# ---------- SRP: сутність книги ----------
@dataclass(frozen=True)
class Book:
    title: str
    author: str
    year: int


class LibraryInterface(Protocol):
    def add_book(self, book: Book) -> None: ...
    def remove_book_by_title(self, title: str) -> bool: ...
    def get_all_books(self) -> List[Book]: ...

    def find(self, predicate: Callable[[Book], bool]) -> List[Book]: ...


class InMemoryLibrary(LibraryInterface):
    def __init__(self) -> None:
        self._books: List[Book] = []

    def add_book(self, book: Book) -> None:
        self._books.append(book)

    def remove_book_by_title(self, title: str) -> bool:
        for i, b in enumerate(self._books):
            if b.title == title:
                del self._books[i]
                return True
        return False

    def get_all_books(self) -> List[Book]:
        # Повертаємо копію, щоб не ламати інваріанти
        return list(self._books)

    def find(self, predicate: Callable[[Book], bool]) -> List[Book]:
        return [b for b in self._books if predicate(b)]


class LoggingLibraryDecorator(LibraryInterface):
    """Додає логування поверх будь-якої реалізації LibraryInterface."""

    def __init__(self, inner: LibraryInterface) -> None:
        self._inner = inner

    def add_book(self, book: Book) -> None:
        logger.info(f"[LOG] add_book: {book}")
        self._inner.add_book(book)

    def remove_book_by_title(self, title: str) -> bool:
        logger.info(f"[LOG] remove_book_by_title: {title}")
        return self._inner.remove_book_by_title(title)

    def get_all_books(self) -> List[Book]:
        books = self._inner.get_all_books()
        logger.info(f"[LOG] get_all_books: {len(books)} items")
        return books

    def find(self, predicate: Callable[[Book], bool]) -> List[Book]:
        results = self._inner.find(predicate)
        logger.info(f"[LOG] find: {len(results)} items")
        return results


# ---------- DIP: високорівневий менеджер залежить від абстракції ----------
class LibraryManager:
    def __init__(self, library: LibraryInterface) -> None:
        self._library = library

    def add(self, title: str, author: str, year: int) -> None:
        self._library.add_book(Book(title=title, author=author, year=year))

    def remove(self, title: str) -> bool:
        return self._library.remove_book_by_title(title)

    def list_all(self) -> List[Book]:
        return self._library.get_all_books()

    def search_by_author(self, author: str) -> List[Book]:
        return self._library.find(lambda b: b.author.lower() == author.lower())


# ---------- UI/CLI шар (окремо від доменної логіки) ----------
def cli_loop(manager: LibraryManager) -> None:
    while True:
        command = (
            input("Enter command (add, remove, show, find_author, exit): ")
            .strip()
            .lower()
        )

        if command == "add":
            title = input("Enter book title: ").strip()
            author = input("Enter book author: ").strip()
            year_str = input("Enter book year: ").strip()
            try:
                manager.add(title, author, int(year_str))
            except ValueError:
                logger.info("Year must be an integer.")
        elif command == "remove":
            title = input("Enter book title to remove: ").strip()
            ok = manager.remove(title)
            if not ok:
                logger.info("Book not found.")
        elif command == "show":
            books = manager.list_all()
            if not books:
                logger.info("(empty)")
            for b in books:
                logger.info(f"Title: {b.title}, Author: {b.author}, Year: {b.year}")
        elif command == "find_author":
            author = input("Enter author: ").strip()
            books = manager.search_by_author(author)
            if not books:
                logger.info("(no results)")
            for b in books:
                logger.info(f"Title: {b.title}, Author: {b.author}, Year: {b.year}")
        elif command == "exit":
            break
        else:
            logger.info("Invalid command. Please try again.")


if __name__ == "__main__":
    base_library = InMemoryLibrary()
    library = LoggingLibraryDecorator(base_library)
    manager = LibraryManager(library)
    cli_loop(manager)
