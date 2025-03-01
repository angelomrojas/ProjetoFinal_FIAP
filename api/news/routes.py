from typing import Annotated

from fastapi import APIRouter, HTTPException, status, Path, Query, Depends
from sqlalchemy.future import select

from .schemas import NewsIn,  NewsGetIn, InteractionsIn, UsersIn, InterecationsList
from .models import User, News, Interactions
from ..database import SessionLocal
import pandas as pd

# Routes.
news_router = APIRouter()

# POST ENDPOINT.
@news_router.post("/news", response_model=NewsIn, status_code=status.HTTP_201_CREATED)
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
@news_router.put("/news", response_model=NewsIn, status_code=status.HTTP_200_OK)
async def update_news_object(news_update: NewsIn):
    id = news_update.model_dump()['page']
    async with SessionLocal() as session:
            query = select(News).where(News.page == id)
            result = await session.execute(query)
            news_obj = result.scalar()
            if news_obj is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Object not found")
            return await News.update(session, news_obj, **news_update.model_dump())
        
        
# GET ENDPOINT
@news_router.get("/news", response_model=list[NewsIn], status_code=status.HTTP_200_OK)
async def get_news_object(theme: Annotated[str | None,  Query(description="Query for theme")] = None):
    filtros = { "theme": theme}
    async with SessionLocal() as session:
            return await News.get(session,**filtros)

#######################################################
#######################################################
#######################################################
#######################################################
#######################################################

# POST ENDPOINT.
@news_router.post("/users", response_model=UsersIn, status_code=status.HTTP_201_CREATED)
async def create_user(create_user: UsersIn):
    async with SessionLocal() as session:
        id = create_user.model_dump()['id']
        async with SessionLocal() as session:
            query = select(User).where(User.id == id)
            result = await session.execute(query)
            user_objs = result.scalar()
        if user_objs is None:
            user_to_create = User(**create_user.model_dump())
            return await User.create(session, user_to_create)
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Object already exists")


#######################################################
#######################################################
#######################################################
#######################################################
#######################################################

# POST ENDPOINT.
# @news_router.post("/interactions", response_model=int, status_code=status.HTTP_201_CREATED)
# async def create_update_interactions(create_interactions: InterecationsList):
    
    
#     async with SessionLocal() as session:
#         for ver in df_dict:
#             print(ver['userId'])
#             query = select(Interactions)
#             query = query.where(Interactions.userId == ver['userId'])
#             query = query.where(Interactions.history == ver['history'])
#             query_ex = await session.execute(query)
#             result = query_ex.scalar()
#             if result is None:
#                 interaction_to_create = User(**ver)
#                 Interactions.create(session, interaction_to_create)
#             else:
#                 News.update(session, result, **ver)
#         raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Object already exists")
    

    
# #######################################################
# #######################################################
# #######################################################
# #######################################################
# #######################################################

# @news_router.post("/recomendacao", response_model=list[NewsIn], status_code=status.HTTP_200_OK)
# async def recommend_object(news_update: InteractionsIn):
#     interacoes = news_update.model_dump()
#     df = pd.DataFrame(interacoes)
#     new_df = df.explode(['history', 'scrollPercentageHistory', 'pageVisitsCountHistory', 'timeOnPageHistory'], ignore_index=True)
#     print (new_df)
    
    
    
#     async with SessionLocal() as session:
#             recommend_list = ['id1', 'id2'] #aqui vai ser modelo
#             query = select(News).filter(News.page.in_(tuple(recommend_list)))
#             result = await session.execute(query)
#             return result.scalars().all()