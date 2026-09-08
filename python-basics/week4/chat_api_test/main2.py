"""main.py：图书管理 API（内存版）"""
from fastapi import FastAPI

app = FastAPI(title="图书管理 API")

# 内存数据（Day 24 换 SQLite）
books = [
    {"id": 1, "title": "Python 入门", "year": 2020},
    {"id": 2, "title": "FastAPI 实战", "year": 2023},
]
next_id = 3

@app.get("/books")
def list_books():
    return books

# 路径参数：/books/1 里的 1 会被装进 book_id
@app.get("/books/{book_id}")
def get_book(book_id: int):
    for b in books:
        if b["id"] == book_id:
            return b
    return {"error": "图书不存在"}, 404    # (内容, 状态码)

# Query 参数：/books/search?year=2023
@app.get("/books/search/")
def search_books(year: int = 0):
    if year == 0:
        return books
    return [b for b in books if b["year"] == year]

@app.post("/books")
def create_book(title: str, year: int):
    global next_id
    book = {"id": next_id, "title": title, "year": year}
    books.append(book)
    next_id += 1
    return book

@app.put("/books/{book_id}")
def update_book(book_id: int, title: str, year: int):
    for i, b in enumerate(books):
        if b["id"] == book_id:
            books[i] = {"id": book_id, "title": title, "year": year}
            return books[i]
    return {"error": "图书不存在"}, 404

@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    for i, b in enumerate(books):
        if b["id"] == book_id:
            removed = books.pop(i)
            return {"deleted": removed}
    return {"error": "图书不存在"}, 404