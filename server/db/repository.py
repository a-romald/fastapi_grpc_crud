import logging
from sqlalchemy import select, insert, delete
from sqlalchemy.exc import SQLAlchemyError

from database import async_session_maker, async_engine
from .model import Article


logging.basicConfig(format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


class BaseRepository:
    model = None

    @classmethod
    async def get_all(cls):
        async with async_session_maker() as session:
            query = select(cls.model)
            result = await session.scalars(query)  # no print() before, called only once, gets all Item objects as a list
            return result.all()


    @classmethod
    async def get_by_id(cls, model_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=model_id)
            result = await session.scalar(query)
            return result


    @classmethod
    async def get_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.scalar(query)
            return result


    @classmethod
    async def search(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.scalars(query)
            return result.all()


    @classmethod
    async def add(cls, data: dict):
        async with async_session_maker() as session:
            if async_engine.dialect.name == "postgresql":
                query = insert(cls.model).values(**data).returning(cls.model.id)
                result = await session.execute(query)
                new_id = result.scalar()   # Returns the first column of the first row
            elif async_engine.dialect.name == "mysql":
                query = insert(cls.model).values(**data)
                result = await session.execute(query)
                new_id = result.inserted_primary_key[0]
            await session.commit()

            query = select(cls.model).filter_by(id=new_id)
            result = await session.scalar(query)
            return result


    @classmethod
    async def update_one_by_id(cls, model_id: int, data: dict):        
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=model_id)
            record = await session.scalar(query)
            for key, value in data.items():
                if value:
                    setattr(record, key, value)
            await session.commit()

            result = await session.scalar(query)
            return result
 

    @classmethod
    async def delete(cls, model_id: int):
        async with async_session_maker() as session:
            query = delete(cls.model).filter_by(id=model_id)
            await session.execute(query)
            await session.commit()


    @classmethod
    async def add_bulk(cls, *data):
        # To load a data array [{"id": 1}, {"id": 2}]
        # we have to handle it through positional arguments *args.
        try:
            query = insert(cls.model).values(*data).returning(cls.model.id)
            async with async_session_maker() as session:
                result = await session.execute(query)
                await session.commit()
                return result.mappings().first()
        except (SQLAlchemyError, Exception) as e:
            if isinstance(e, SQLAlchemyError):
                msg = "Database Exc"
            elif isinstance(e, Exception):
                msg = "Unknown Exc"
            msg += ": Cannot bulk insert data into table"

            logger.error(msg, extra={"table": cls.model.__tablename__}, exc_info=True)
            return None


class ArticleRepository(BaseRepository):
    model = Article

    @classmethod
    async def update_one_by_id(cls, model_id: int, data: dict):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=model_id)
            record = await session.scalar(query)
            for key, value in data.items():
                if key == 'published':
                    setattr(record, key, value)
                else:
                    if value:
                        setattr(record, key, value)
            await session.commit()            

            result = await session.scalar(query)
            return result
