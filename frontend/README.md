# FastAPI Project - Frontend

## 开发环境配置

安装依赖，使用 `node@20`: 

```shell
npm install
```

确认 `.env` 中的后端服务接口，启动服务：

```shell
npm run dev
```

## 生产环境部署

拉取最新的 `master` 分支代码，或需要的 `tag` 版本代码，使用 `Docker Compose` 启动：

```shell
cd frontend
docker compose up -d
```
