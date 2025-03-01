from fastapi import FastAPI
from http import HTTPStatus
from api.database import engine
import uvicorn

from api.news.routes import news_router
from api.database import Base

app = FastAPI()

app.include_router(news_router, prefix="", tags=['news'])

@app.get("/health", status_code=200)
async def root():
    return HTTPStatus.OK


if __name__ == '__main__':
    uvicorn.run("main:app", reload=False, host="127.0.0.1", port=8000)