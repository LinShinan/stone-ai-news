from sqlalchemy.ext.asyncio import AsyncSession
from models.news import Category, News
from sqlalchemy import select, func,update


async def get_categories(db: AsyncSession, skip: int =0 ,limit: int=10):
    res = await db.execute(select(Category).offset(skip).limit(limit))
    return res.scalars().all()

async def  get_page_news(db: AsyncSession, category_id: int, skip: int =0, limit: int =10):
    statm = select(News).where(News.category_id == category_id).offset(skip).limit(limit)
    res = await db.execute(statm)
    return res.scalars().all()

async def get_news_count(db: AsyncSession, category_id: int):
    statm = select(func.count(News.id)).where(News.category_id == category_id)
    res = await db.execute(statm)
    return res.scalar_one()


async def get_news_by_id(db: AsyncSession, news_id: int):
    statm = select(News).where(News.id == news_id)
    res = await db.execute(statm)
    return res.scalar_one_or_none()

async def increase_views(db: AsyncSession,news_id: int):
    stmt = update(News).where(News.id==news_id).values(views=News.views+1)
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount > 0

async def get_related_news(db: AsyncSession, category_id: int, exclude_id: int, limit: int = 5):
    statm = (
        select(News)
        .where(News.category_id == category_id, News.id != exclude_id)
        .order_by(News.publish_time.desc())
        .limit(limit)
    )
    res = await db.execute(statm)
    return res.scalars().all()
