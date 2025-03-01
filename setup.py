# python libs
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# api lib
from api.news.models import News
from api.config import settings
from api.database import Base

# data lib
# from data import news_pipeline


async def create_tables(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# def run_pipe(pipeline, url_path):
#         return pipeline(url_path)

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

    # create tables on db
    await create_tables(engine)


    #news = news_pipeline().to_dict(orient='records')



    # async with SessionLocal() as session:
    #     await insert_data(session, news, News)
 

    await engine.dispose()
    

if __name__ == '__main__':
# Run the main function synchronously
    asyncio.run(main())