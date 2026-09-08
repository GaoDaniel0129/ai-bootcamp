# ===== 构建阶段 1：装依赖 =====
FROM python:3.12-slim AS builder
# 基础镜像：官方 Python 精简版（你的 RHEL 上也能拉，镜像自带运行环境）
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# ===== 构建阶段 2：精简运行镜像 =====
FROM python:3.12-slim
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
# 只拷依赖，不拷构建缓存 → 镜像更小
COPY . .
# 告诉 Docker：容器里服务监听 8000 端口
EXPOSE 8000
# 启动命令：uvicorn 跑起来（0.0.0.0 让容器外能访问）
CMD ["python", "-m", "uvicorn", "main6:app", "--host", "0.0.0.0", "--port", "8000"]