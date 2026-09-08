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