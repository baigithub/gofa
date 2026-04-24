# 后端 OpenAPI 文档说明

## 访问方式

启动后端服务后访问：

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- OpenAPI JSON: `http://localhost:8000/openapi.json`

## 已补充内容

- 接口分组标签说明（`auth` / `orders` / `payments` / `runner`）
- 关键请求体示例：
  - `POST /api/v1/auth/send-code`
  - `POST /api/v1/auth/login`
  - `POST /api/v1/orders`
  - `POST /api/v1/payments/create`
  - `POST /api/v1/payments/wechat/callback`
- 统一响应结构：
  - `code`: 业务码（成功为 `0`）
  - `message`: 描述信息
  - `data`: 业务数据

## 常用调试接口

- 健康检查：`GET /health`
- 数据库连通：`GET /db/ping`

