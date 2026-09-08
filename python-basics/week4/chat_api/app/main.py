"""main.py：聊天 API v1（会话存 SQLite）"""
from uuid import uuid4
from fastapi import FastAPI
from pydantic import BaseModel, Field
import db
import llm_liushi
import json
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
import pathlib

app = FastAPI(title="Chat API")
db.init_db()
app.mount("/static", StaticFiles(directory=pathlib.Path(__file__).parent / "static"), name="static")

SYSTEM_PROMPT = "你是 Daniel 的 AI 助手，回答简洁专业，用中文。"

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)
    session_id: str = "new"        # 客户端不传就开新会话

@app.post("/chat")
def chat(req: ChatRequest):
    # 1. 开新会话 or 续旧会话
    if req.session_id == "new":
        session_id = str(uuid4())
        db.save_message(session_id, "system", SYSTEM_PROMPT)
    else:
        session_id = req.session_id

    # 2. 取历史 + 新消息，拼 messages
    history = db.get_history(session_id)
    messages = history + [{"role": "user", "content": req.message}]

    # 3. 调 LLM
    reply = llm_liushi.ask_llm(messages)

    # 4. 入库（用户消息和 AI 回复都要存！）
    db.save_message(session_id, "user", req.message)
    db.save_message(session_id, "assistant", reply)

    return {"session_id": session_id, "reply": reply}

@app.get("/sessions/{session_id}/messages")
def get_session_messages(session_id: str):
    return db.get_history(session_id, limit=100)

@app.delete("/sessions/{session_id}")
def clear_session(session_id: str):
    db.clear_session(session_id)
    return {"cleared": session_id}

@app.post("/chat/stream")
def chat_stream(req: ChatRequest):
    if req.session_id == "new":
        session_id = str(uuid4())
        db.save_message(session_id, "system", SYSTEM_PROMPT)
    else:
        session_id = req.session_id

    history = db.get_history(session_id)
    messages = history + [{"role": "user", "content": req.message}]
    db.save_message(session_id, "user", req.message)

    def event_stream():
        full_reply = ""
        for piece in llm_liushi.ask_llm_stream(messages):
            full_reply += piece
            # SSE 事件：包一层 JSON，方便前端解析
            yield f"data: {json.dumps({'delta': piece}, ensure_ascii=False)}\n\n"
        # 收尾：把完整回答存库
        db.save_message(session_id, "assistant", full_reply)
        yield f"data: {json.dumps({'done': True})}\n\n"

    return StreamingResponse(event_stream(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache"})

"""main.py 追加"""
from fastapi import Depends, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import auth, db
from fastapi import HTTPException

security = HTTPBearer()   # 让 /docs 能带 token 测试

class RegisterRequest(BaseModel):
    username: str
    password: str

@app.post("/register")
def register(req: RegisterRequest):
    ok = db.create_user(req.username, req.password)
    if not ok:
        raise HTTPException(status_code=400, detail="用户名已存在")
    return {"message": "注册成功，请登录"}

@app.post("/login")
def login(req: RegisterRequest):
    user = db.get_user(req.username)
    if not user or not db.verify_password(req.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    token = auth.create_token(user["id"], user["username"])
    return {"access_token": token, "token_type": "bearer"}

def require_user(cred: HTTPAuthorizationCredentials = Depends(security)):
    """依赖：任何接口加这个参数，就自动要求带合法 token"""
    try:
        payload = auth.decode_token(cred.credentials)
        return payload
    except Exception:
        raise HTTPException(status_code=401, detail="token 无效或已过期")

# 受保护的接口：加一个 require_user 参数即可
@app.post("/chat/protected")
def chat_protected(req: ChatRequest, user: dict = Depends(require_user)):
    # 把 user 存进消息历史，实现"按用户隔离会话"——TODO Day 28 完善
    return chat(req)