from __future__ import annotations

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.future import select

from ..database import Base


class News(Base):

    __tablename__ = "news"
    id = Column(Integer, primary_key=True)
    page = Column(String())
    url = Column(String())
    issued = Column(DateTime)
    modified = Column(DateTime)
    title = Column(String())
    body = Column(String())
    caption = Column(String())

    def __repr__(self):
        return f"{self.title}"
    
    @classmethod
    async def create(cls, session, obj_to_create):
        session.add(obj_to_create)
        await session.commit()
        return obj_to_create
    
    async def get_by_id(cls, session, id):
        query = select(cls).where(cls.page == id)
        result = await session.execute(query)
        comercio_obj = result.scalar()
        return comercio_obj
    
    @classmethod
    async def update(cls, session, old_obj, **new_obj):
        for field, value in new_obj.items():
            if field=='page':
                continue
            setattr(old_obj, field, value)
        await session.commit()
        return old_obj
    
    @classmethod
    async def delete(cls, session, obj_to_delete):
        await session.delete(obj_to_delete)
        await session.commit()
    
    
class User(Base):

    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    id_default = Column(String(200))

    def __repr__(self):
        return f"{self.id}"
    
    @classmethod
    async def get(cls, session, **kwargs):
        query = select(cls)
        result = await session.execute(query)
        return result.scalars().all()
    
    @classmethod
    async def get_by_id(cls, session, id):
        query = select(cls).where(cls.id == id)
        result = await session.execute(query)
        comercio_obj = result.scalar()
        return comercio_obj
    
    @classmethod
    async def create(cls, session, obj_to_create):
        session.add(obj_to_create)
        await session.commit()
        return obj_to_create
    
    @classmethod
    async def update(cls, session, old_obj, **new_obj):
        for field, value in new_obj.items():
            setattr(old_obj, field, value)
        await session.commit()
        return old_obj
    
    @classmethod
    async def delete(cls, session, obj_to_delete):
        await session.delete(obj_to_delete)
        await session.commit()
    
    
class Interactions(Base):

    __tablename__ = "interactions"

    id = Column(Integer, primary_key=True , autoincrement=True)
    userId = Column(String(200), ForeignKey(User.id_default))
    history = Column(String(200), ForeignKey(News.page))
    scrollPercentageHistory = Column(Float)
    pageVisitsCountHistory = Column(Integer)
    timeOnPageHistory = Column(String(200))

    def __repr__(self):
        return f"{self.userId} - {self.history}"
    
    @classmethod
    async def get(cls, session, **kwargs):
        query = select(cls)
        if kwargs.get('userId') is not None:
            query = query.where(cls.theme == kwargs.get('userId'))
        if kwargs.get('history') is not None:
            query = query.where(cls.theme == kwargs.get('history'))
        result = await session.execute(query)
        return result.scalars().all()
    
    async def get_by_id(cls, session, id):
        query = select(cls).where(cls.id == id)
        result = await session.execute(query)
        comercio_obj = result.scalar()
        return comercio_obj
    
    @classmethod
    async def create(cls, session, obj_to_create):
        session.add(obj_to_create)
        await session.commit()
        return obj_to_create
    
    @classmethod
    async def update(cls, session, old_obj, **new_obj):
        for field, value in new_obj.items():
            setattr(old_obj, field, value)
        await session.commit()
        return old_obj
    
    @classmethod
    async def delete(cls, session, obj_to_delete):
        await session.delete(obj_to_delete)
        await session.commit()
        
    
    
    
