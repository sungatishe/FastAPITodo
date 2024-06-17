from typing import Optional

from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int

    def __init__(self, id, title, author, description, rating):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating


class BookRequest(BaseModel):
    id: Optional[int] = Field(title='is not indeed')
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(max_length=100, min_length=1)
    rating: int = Field(gt=0, lt=6)

    class Config:
        json_schema_extra = {
            'example': {
                "id": 11,
                "title": "Melancholy",
                "author": "Yasashi Kimomoto",
                "description": "Good book about Melancholic days of Yasashi",
                "rating": 4
            }
        }


BOOKS = [
    Book(1, "To Kill a Mockingbird", "Harper Lee", "A novel about the serious issues of rape and racial inequality.",
         5),
    Book(2, "1984", "George Orwell", "A dystopian social science fiction novel and cautionary tale about the future.",
         5),
    Book(3, "Pride and Prejudice", "Jane Austen", "A romantic novel of manners that depicts the British Regency era.",
         4),
    Book(4, "The Great Gatsby", "F. Scott Fitzgerald", "A story about the young and mysterious millionaire Jay Gatsby "
                                                       "and his quixotic passion for the beautiful Daisy Buchanan.", 4),
    Book(5, "Moby Dick", "Herman Melville", "The narrative of Captain Ahab's obsessive quest to kill the giant white "
                                            "whale, Moby Dick.", 4),
    Book(6, "War and Peace", "Leo Tolstoy", "A historical novel that tells the story of five families during the "
                                            "Napoleonic wars.", 5),
    Book(7, "The Catcher in the Rye", "J.D. Salinger", "A novel about teenage rebellion and alienation.", 4),
    Book(8, "The Hobbit", "J.R.R. Tolkien", "A fantasy novel and prelude to The Lord of the Rings, featuring the "
                                            "adventures of Bilbo Baggins.", 5),
    Book(9, "Crime and Punishment", "Fyodor Dostoevsky", "A philosophical novel exploring themes of morality, guilt, "
                                                         "and redemption.", 5),
    Book(10, "The Brothers Karamazov", "Fyodor Dostoevsky", "A complex novel that deals with deep philosophical and "
                                                            "spiritual issues.", 5)
]


@app.get('/books')
async def get_books():
    return BOOKS


@app.get('/books/{book_id}')
async def read_book(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book

    raise HTTPException(status_code=404, detail='Item has not found')


@app.post('/books/create/')
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))


@app.get('/books/rating/')
async def get_books_by_rating(books_rating: int = Query(gt=0, lt=6)):
    books_ratings = []
    for book in BOOKS:
        if book.rating == books_rating:
            books_ratings.append(book)

    return books_ratings


def find_book_id(book: Book):
    if len(BOOKS) > 0:
        book.id = BOOKS[-1].id + 1
    else:
        book.id = 1

    return book


@app.put('/books/update/')
async def update_book(book: BookRequest):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
            book_changed = True
    if not book_changed:
        raise HTTPException(status_code=404, detail='Item not found')


@app.delete('/books/delete/')
async def delete_book(book_id: int = Path(gt=0)):
    book_deleted = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            book_deleted = True
    if not book_deleted:
        raise HTTPException(status_code=404, detail='Item not found')
