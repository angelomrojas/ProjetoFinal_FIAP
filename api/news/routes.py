from typing import Annotated

from fastapi import APIRouter, HTTPException, status, Path, Query, Depends
from sqlalchemy.future import select

from .schemas import NewsIn,  NewsGetIn, InteractionsIn, UsersIn, InterecationsList, Recommend
from .models import User, News, Interactions
from ..database import SessionLocal
import pandas as pd
from api.prediction import load_model

model = load_model()

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

#CREATE OR UPDATE ENDPOINT.
@news_router.post("/interactions", response_model=int, status_code=status.HTTP_201_CREATED)
async def create_update_or_create_interactions(create_interactions: InterecationsList):
    
    
    async with SessionLocal() as session:
        novas_interactions = create_interactions.model_dump()
        for interactions in novas_interactions['Interecation']:
            query = select(Interactions)
            query = query.where(Interactions.userId == interactions['userId'])
            query = query.where(Interactions.history == interactions['history'])
            query_ex = await session.execute(query)
            result = query_ex.scalar()
            if result is None:
                interaction_to_create = Interactions(**interactions)
                await Interactions.create(session, interaction_to_create)
            else:
                await Interactions.update(session, result, **interactions)
        return 1
    
    

    
# #######################################################
# #######################################################
# #######################################################
# #######################################################
# #######################################################

@news_router.post("/recomendacao", status_code=status.HTTP_200_OK)
async def recommend_object(recommend: Recommend):
    async with SessionLocal() as session:
        rec = recommend.model_dump()
        
        query = select(News.id, News.page).where(News.page.in_(rec["news_id"])).distinct()
        result = await session.execute(query)
        result = list(result)
        news = [row[0] for row in result]
        news_default = [row[1] for row in result]

        dimensão = len(news)
            
        query = select(User.id).where(User.id_default.in_(rec["user_id"])).distinct()
        result = await session.execute(query)
        users = [row[0] for row in result]
        users = users*dimensão
           
           
        resposta = model.predict(users, news)
        lista_resposta = [int(i) for i in resposta[0]]
        return dict(zip(news_default, lista_resposta))


    
        
        
        
    
       