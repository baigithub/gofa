# Gofer Backend（FastAPI）

## 一键启动（推荐）

在项目根目录执行：

```bash
# 1) 启动基础服务（MySQL + Redis）
cp .env.example .env
docker compose up -d

# 2) 初始化后端环境文件
cp backend/.env.local.example backend/.env.local

# 3) 首次初始化数据库（可选其一：Alembic 或 SQL）
# 方式A：Alembic（推荐）
alembic -c backend/alembic.ini upgrade head

# 方式B：直接执行SQL
docker exec -i gofer-mysql mysql -uroot -proot123456 < backend/sql/init.sql

# 4) 启动后端服务
source .venv/bin/activate
uvicorn backend.app.main:app --reload --port 8000
```

启动后访问：

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`
- OpenAPI JSON: `http://127.0.0.1:8000/openapi.json`
- 健康检查: `http://127.0.0.1:8000/health`

## 环境配置说明

后端使用 `.env` / `.env.local` 读取环境变量，变量前缀统一为 `GOFER_`。

- 推荐：复制 `backend/.env.local.example` 为 `backend/.env.local` 并按需修改
- 测试环境：参考 `backend/.env.test.example`

### 必要变量

- `GOFER_DATABASE_URL`：数据库连接串（MySQL，Docker 中 root 密码为 `root123456`）
- 根目录 `.env` 中 `GOFER_MYSQL_PORT`：Docker 映射端口（默认 `3307`，用于避免本机 `3306` 冲突）

示例：

```env
GOFER_DATABASE_URL=mysql+pymysql://root:root123456@127.0.0.1:3307/gofer?charset=utf8mb4
```

## 常用命令

在项目根目录执行：

```bash
# 启动/停止基础服务
docker compose up -d
docker compose down

# 查看容器状态
docker compose ps

# 运行测试
PYTHONPATH=$(pwd) pytest backend/tests -q

# 本地开发启动
source .venv/bin/activate
uvicorn backend.app.main:app --reload --port 8000
```

## 联通性验证

执行以下命令验证数据库连通：

```bash
python -c "from backend.app.core.db import engine; from sqlalchemy import text; conn=engine.connect(); print(conn.execute(text('SELECT 1')).scalar()); conn.close()"
```

输出为 `1` 即表示数据库连接成功。

