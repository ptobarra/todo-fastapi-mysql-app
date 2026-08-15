from typing import Annotated

from fastapi import Body, FastAPI

app = FastAPI()

BOOKS = [
    {"title": "Title One", "author": "Author One", "category": "science"},
    {"title": "Title Two", "author": "Author Two", "category": "science"},
    {"title": "Title Three", "author": "Author Three", "category": "history"},
    {"title": "Title Four", "author": "Author Four", "category": "math"},
    {"title": "Title Five", "author": "Author Five", "category": "math"},
    {"title": "Title Six", "author": "Author Two", "category": "math"},
]

# @app.get("/api-endpoint")
# def first_api(): # async is optional with fastapi
# async def first_api():
#     return {"message": "Hello Eric!"}


@app.get("/books")
async def read_all_books():
    return BOOKS


# in this case, we have a static path that is the same as the dynamic path,
# so we need to put the static path first, otherwise it will never be
# reached because the dynamic path will always match first.
# @app.get("/books/mybook")
# async def read_all_books():
#     return {'book_title': 'My favorite book!'}

# @app.get("/books/{dynamic_param}")
# async def read_all_books(dynamic_param: str):
#     return {'dynamic_param': dynamic_param}


@app.get("/books/{book_title}")
async def read_book_by_title(book_title: str):
    for book in BOOKS:
        if book.get("title").casefold() == book_title.casefold():
            return book


# think of a query parameter as a way to filter data based on the URL provided.


@app.get("/books/")
async def read_book_by_query(category: str):
    books_to_return = []
    for book in BOOKS:
        if book.get("category").casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return


# The smaller API endpoints must always be defined before the larger API
# endpoints, otherwise the smaller API endpoints will never be reached
# because the larger API endpoints taking more vairables will always match
# first. So the smaller API endpoints will never be reached.

# Create a new API Endpoint that can fetch all books from a specific author
# using either Path Parameters or Query Parameters.


# Query Parameter Example: /books/byauthor?author=Author%20Two
@app.get("/books/byauthor/")
async def read_books_by_author_query(author: str):
    books_to_return = []
    for book in BOOKS:
        if book.get("author").casefold() == author.casefold():
            books_to_return.append(book)
    return books_to_return


# we are going to pass author as a path parameter and category as a query
# parameter. This is a common pattern in REST APIs, where you use path
# parameters to identify a specific location and query parameters to filter
# whatever data you want to return.


@app.get("/books/{book_author}/")
async def read_author_category_by_query(book_author: str, category: str):
    books_to_return = []
    for book in BOOKS:
        if (
            book.get("author").casefold() == book_author.casefold()
            and book.get("category").casefold() == category.casefold()
        ):
            books_to_return.append(book)
    return books_to_return


# POST is the create HTTP method, and it is used to be able to send more
# data through an API endpoint. So that we can essentially be able to
# create pieces of data.
# GET cannot have a body, but POST can have a body. So we can send more
# data through the body of the request.
# JSON data in HTTP body must be enclosed in double quotes, keys and values
# the structure of the data that we send in the body of the request must
# match the structure of the data that we are storing in our BOOKS list. So
# we need to make sure that we are sending a JSON object with the same keys
# as the other books in our BOOKS list.


@app.post("/books/create_book")
async def create_book(new_book: Annotated[dict, Body()]):
    BOOKS.append(new_book)


# PUT is equivalent to update, and it is used to update existing data. So we
# can use PUT to update an existing book in our BOOKS list.


@app.put("/books/update_book")
async def update_book(updated_book: Annotated[dict, Body()]):
    for i in range(len(BOOKS)):
        if BOOKS[i].get("title").casefold() == updated_book.get("title").casefold():
            BOOKS[i] = updated_book


@app.delete("/books/delete_book/{book_title}")
async def delete_book(book_title: str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get("title").casefold() == book_title.casefold():
            BOOKS.pop(i)
            break


# Create a new API Endpoint that can fetch all books from a specific author
# using either Path Parameters or Query Parameters.


# Path Parameter Example: /books/byauthor/Author%20Two
@app.get("/books/byauthor/{book_author}")
async def read_books_by_author_path(book_author: str):
    books_to_return = []
    for book in BOOKS:
        if book.get("author").casefold() == book_author.casefold():
            books_to_return.append(book)
    return books_to_return


# uvicorn books:app --reload
# fastapi run books.py
# fastapi dev books.py - spins up a development server

# %20 means space in a URL, so if you want to search for "Title One", you
# would need to use "Title%20One" in the URL.
