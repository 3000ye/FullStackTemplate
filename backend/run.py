import uvicorn
from fastapi import FastAPI, Request
from datetime import datetime
from starlette.middleware.cors import CORSMiddleware

from backend.api.main import api_router
from backend.utils.logger import Logger

logger = Logger(name=__name__)


def create() -> FastAPI:
    application = FastAPI(title="Full Stack Template", docs_url="/docs")
    application.debug = True

    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # 允许所有来源
        allow_methods=["*"],  # 允许所有方法
        allow_headers=["*"],  # 允许所有请求头
        allow_credentials=True,
    )

    # Add middleware for logging request time
    @application.middleware("http")
    async def log_request_time(request: Request, call_next):
        access_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Access Time: {access_time}, Path: {request.url.path}, Method: {request.method}")
        response = await call_next(request)
        return response


    application.include_router(api_router, prefix="/api")

    return application


# reload 模式
app = create()
if __name__ == "__main__":
    uvicorn.run(app="run:app", host="0.0.0.0", port=3336, reload=True)
