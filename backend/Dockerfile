FROM python:3.11-slim

WORKDIR /app

# 安装系统依赖（PDF/Word 解析、编译所需）
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# 安装 uv
RUN pip install --no-cache-dir uv

# 复制依赖文件
COPY pyproject.toml uv.lock* ./

# 使用 uv sync 安装依赖（更快、更可靠）
RUN uv sync --no-dev || uv pip install --system -r pyproject.toml

COPY . .

EXPOSE 8000

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers"]