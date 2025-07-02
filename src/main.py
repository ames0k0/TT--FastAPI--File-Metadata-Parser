import uvicorn
from fastapi import FastAPI

from core.config import settings
from core.dependencies import lifespan
from routers import routers


app = FastAPI(
    lifespan=lifespan,
    title="Тестовое задания",
    summary="REST API для запуска парсинга и получения сохранённых данных​",
    debug=True,
)

for router in routers:
    app.include_router(router=router)


if __name__ == "__main__":
    uvicorn.run(
        app=app,
        host=settings.APP_HOST,
        port=settings.APP_PORT,
    )
