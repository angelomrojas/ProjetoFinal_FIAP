# python libs
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import pandas as pd

# api lib
from api.news.models import News, Interactions, User
from api.config import settings
from api.database import Base





async def create_tables(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


def run_pipe(pipeline, url_path):
        return pipeline(url_path)

# Define async function for batch insertion into multiple tables
async def insert_data(session, data, table):
    async with session.begin():
        # Create the insert statement
        insert_stmt = table.__table__.insert().values(data)
        # Execute the insert statement
        await session.execute(insert_stmt)



async def main():
    engine = create_async_engine(
        settings.DATABASE_URL, 
        pool_pre_ping=True,
        pool_recycle=3600
    )

    SessionLocal = sessionmaker(
        bind=engine,
        expire_on_commit=False,
        future=True,
        class_=AsyncSession 
    )

    # # create tables on db
    await create_tables(engine)


    df_train = pd.read_csv("train.csv")
    df_user = df_train[['userId', 'user_id']].copy()
    df_user = df_user.rename(columns={"userId": "id", "user_id": "id_default"})

    df_interactions = df_train[['user_id', 'history_','scrollPercentageHistory','pageVisitsCountHistory','timeOnPageHistory']].copy()
    df_interactions = df_interactions.rename(columns={"user_id": "userId", "history_": "history"})


    df_news = pd.read_csv("news.csv")
    df_news = df_news[['page','url','issued','modified','title','body','caption']]

    df_relacao = df_train[['history_','history']]
    df_relacao = df_relacao.rename(columns={"history_": "page", "history": "id"})
    df_relacao.drop_duplicates(inplace=True)

    df_final = df_news.merge(df_relacao, on="page", how="left")
    colunas = ["id"] + [col for col in df_final.columns if col != "id"]
    df_final['issued'] = pd.to_datetime(df_final['issued'])
    df_final['modified'] = pd.to_datetime(df_final['modified'])
    df_final = df_final[colunas]


    news = df_final.to_dict(orient='records')
    users = df_user.to_dict(orient='records')
    interactions = df_interactions.to_dict(orient='records')
    
    async with SessionLocal() as session:
        for i in range(0, len(news), 900):
            news_i = news[i:i+900]
            await insert_data(session, news_i, News)
        await session.commit()  # Fazer o commit após inserir todos os lotes

    async with SessionLocal() as session:
        for i in range(0, len(users), 900):
            users_i = users[i:i+900]
            await insert_data(session, users_i, User)
        await session.commit()

    async with SessionLocal() as session:
        for i in range(0, len(interactions), 900):
            interactions_i = interactions[i:i+900]
            await insert_data(session, interactions_i, Interactions)
        await session.commit()

    await engine.dispose()
    

if __name__ == '__main__':
# Run the main function synchronously
    asyncio.run(main())