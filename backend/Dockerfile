FROM python:3.11-slim

WORKDIR /app

# 安装系统依赖（PDF/Word 解析所需）
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml uv.lock* ./

# 安装 uv 并同步依赖
RUN pip install --no-cache-dir uv && \
    uv pip install --system -r pyproject.toml || \
    pip install --no-cache-dir .

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
