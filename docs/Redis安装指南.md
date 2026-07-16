# Redis 安装与启动指南

## Windows 本地安装

### 方法一：使用 MSYS2 安装（推荐）

1. 安装 MSYS2（如果尚未安装）：https://www.msys2.org/
2. 打开 MSYS2 UCRT64 终端
3. 执行：
   ```bash
   pacman -S mingw-w64-ucrt-x86_64-redis
   ```
4. 启动 Redis：
   ```bash
   redis-server
   ```

### 方法二：使用 WSL2（Linux子系统）

1. 安装 WSL2 和 Ubuntu：
   ```powershell
   wsl --install -d Ubuntu
   ```
2. 在 Ubuntu 中安装 Redis：
   ```bash
   sudo apt update
   sudo apt install redis-server
   sudo service redis-server start
   ```
3. Redis 将在 localhost:6379 运行

### 方法三：使用 Docker

```bash
docker run -d --name redis -p 6379:6379 redis:7-alpine
```

### 方法四：下载 Windows 原生版本

1. 下载：https://github.com/tporadowski/redis/releases
2. 解压后运行 `redis-server.exe`

## Docker Compose 方式（完整环境）

```bash
docker-compose up -d redis
```

## 验证连接

```bash
redis-cli ping
# 应返回 PONG
```

## 配置说明

项目默认 Redis 连接配置：
- URL: `redis://localhost:6379/0`
- 可通过 `.env` 中的 `REDIS_URL` 修改

Redis 不可用时，系统会自动降级，不影响核心功能。
