# 應用Dockerfile
FROM python:3.11-slim-bookworm

WORKDIR /usr/src/app


# 安裝依賴（Oracle 驅動使用 thin mode，不需要 Oracle Instant Client）
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    libaio1 \
    python3-dev \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*
# 安裝 uv
RUN pip install --no-cache-dir uv

# 複製你的專案依賴信息
# 應確保你的專案中有 pyproject.toml 以及 uv.lock
COPY pyproject.toml uv.lock ./

# 安裝依賴（依照 lock 檔確保完全一致）
RUN uv sync --locked

#複製你的後端代碼到容器中
COPY . .

# 啟動後執行你的後端 (比如說FastAPI)
ENTRYPOINT ["uvicorn"]
CMD ["main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
