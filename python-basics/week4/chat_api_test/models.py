"""models.py：请求/响应模型"""
from pydantic import BaseModel, Field

class BookCreate(BaseModel):
    """创建图书的请求体"""
    title: str = Field(..., min_length=1, max_length=100, description="书名")
    # Field(...) 的 ... 表示"必填"
    year: int = Field(..., ge=1900, le=2100, description="出版年份")
    # ge = greater equal（≥1900） le = less equal（≤2100）

class BookUpdate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    year: int = Field(..., ge=1900, le=2100)

class BookOut(BaseModel):
    """返回给用户的模型（id 会由服务端生成）"""
    id: int
    title: str
    year: int