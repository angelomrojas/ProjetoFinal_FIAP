from typing import Annotated

from fastapi import APIRouter, HTTPException, status, Path, Query, Depends
from sqlalchemy.future import select

from .schemas import NewsIn
from .models import User, News, Interactions
from ..database import SessionLocal


# Routes.
news_router = APIRouter()

# POST ENDPOINT.
@news_router.post("/", response_model=NewsIn, status_code=status.HTTP_201_CREATED)
async def create_news(create_news: NewsIn):
    async with SessionLocal() as session:
        id = create_news.model_dump()['page']
        async with SessionLocal() as session:
            query = select(News).where(News.page == id)
            result = await session.execute(query)
            news_objs = result.scalar()
        if news_objs is None:
            news_to_create = News(**create_news.model_dump())
            return await News.create(session, news_to_create)
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Object already exists")


# UPDATE ENDPOINT
@news_router.put("/{id}", response_model=NewsIn, status_code=status.HTTP_200_OK)
async def update_news_object(news_update: NewsIn):
    id = news_update.model_dump()['page']
    async with SessionLocal() as session:
            query = select(News).where(News.page == id)
            result = await session.execute(query)
            news_obj = result.scalar()
            if news_obj is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Object not found")
    return await News.update(session, news_obj, **news_update.model_dump())