from fastapi import FastAPI

app = FastAPI(title="图书管理 API")   # app 是 FastAPI 的"应用实例"

@app.get("/")                          # 装饰器：把函数绑定到 GET /
def root():
    return {"message": "Hello AI 工程师"}

@app.get("/books")                     # GET /books → 返回全部图书
def list_books():
    return books

# 内存"数据库"（Day 24 换成 SQLite）
books = [{"id": 1, "title": "Python 入门", "year": 2020}]