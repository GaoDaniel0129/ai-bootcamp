"""main.py：图书管理 API（Pydantic 版）"""
from fastapi import FastAPI, HTTPException
from models import BookCreate, BookUpdate, BookOut

app = FastAPI(title="图书管理 API")

books = [{"id": 1, "title": "Python 入门", "year": 2020}]
next_id = 2

@app.get("/books", response_model=list[BookOut])
def list_books():
    return books

@app.post("/books", response_model=BookOut, status_code=201)
def create_book(payload: BookCreate):      # ★ 请求体会被自动校验成 BookCreate
    global next_id
    book = {"id": next_id, **payload.model_dump()}   # model_dump() = 转成字典
    books.append(book)
    next_id += 1
    return book

@app.put("/books/{book_id}", response_model=BookOut)
def update_book(book_id: int, payload: BookUpdate):
    for i, b in enumerate(books):
        if b["id"] == book_id:
            books[i] = {"id": book_id, **payload.model_dump()}
            return books[i]
    # 规范做法：抛 HTTPException，而不是返回 (dict, 404)
    raise HTTPException(status_code=404, detail=f"图书 {book_id} 不存在")

@app.delete("/books/{book_id}", status_code=204)
def delete_book(book_id: int):
    for i, b in enumerate(books):
        if b["id"] == book_id:
            books.pop(i)
            return
    raise HTTPException(status_code=404, detail=f"图书 {book_id} 不存在")