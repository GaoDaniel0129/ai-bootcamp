# Chat API —— AI 多轮对话服务（项目 1）

基于 FastAPI 的大模型对话 API：多轮记忆、流式输出（SSE）、JWT 鉴权、Docker 一键部署。

## 功能
- POST /chat：多轮对话（SQLite 持久化，重启不丢）
- POST /chat/stream：SSE 流式输出
- POST /register、/login：JWT 注册登录
- /chat/protected：需 token 访问（示例）
- 交互式文档：/docs（Swagger）

## 技术栈
FastAPI · SQLite · DeepSeek API · SSE · PyJWT · Docker

## 架构
浏览器/客户端 → FastAPI(路由+鉴权) → LLM 服务
                        ↓
                  SQLite(会话/用户)

## 快速开始
\`\`\`bash
export DEEPSEEK_API_KEY=sk-xxx
docker compose up -d --build
# 打开 http://localhost:8000/docs
\`\`\`

## 目录结构
chat_api/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI 实例 + 路由（薄）
│   ├── config.py        # 所有配置：API_KEY/SECRET/数据库路径
│   ├── db.py            # 数据层
│   ├── auth.py          # JWT + 密码哈希
│   ├── llm.py           # 模型调用（流式/非流式/工具）
│   ├── schemas.py       # Pydantic 模型（原 models.py）
│   └── static/index.html
├── data/                # SQLite 文件目录（.gitignore 掉）
├── tests/               # 放 1 个冒烟测试（见 28.5）
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md

## 截图
（放 /docs 页面和流式聊天页截图）

## 已上线地址
http://服务器IP:8000/docs