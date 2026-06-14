from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from config.mysql_conf import get_db
from crud.news import get_categories, get_news_by_id, get_news_count, get_page_news, get_related_news, increase_views
from schemas.news import CategoryResponse, NewsDetailData, NewsDetailItem, NewsListData, NewsResponse
from schemas.response import Result

router = APIRouter(prefix="/api/news", tags=["news"])


@router.get("/categories", response_model=Result[list[CategoryResponse]])
async def list_categories(
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_db),
):
    """查询分类列表"""
    data = await get_categories(db, skip=skip, limit=limit)
    return Result.ok([CategoryResponse.model_validate(c) for c in data])


@router.get("/list", response_model=Result[NewsListData])
async def list_news(
    category_id: int = Query(..., alias="categoryId"),
    page: int = 1,
    page_size: int = Query(10, alias="pageSize"),
    db: AsyncSession = Depends(get_db),
):
    """分页查询新闻列表"""
    skip = (page - 1) * page_size
    news = await get_page_news(db, category_id, skip, page_size)
    total = await get_news_count(db, category_id)
    has_more = total > (skip + len(news))
    return Result.ok(
        NewsListData(
            list=[NewsResponse.model_validate(n) for n in news],
            total=total,
            hasMore=has_more,
        )
    )

@router.get("/detail", response_model=Result[NewsDetailData])
async def get_news_detail(
    id: int = Query(..., description="新闻ID"),
    db: AsyncSession = Depends(get_db),
):
    """查询新闻详情"""
    news = await get_news_by_id(db, id)
    if not news:
        return Result.fail(code=404, message="新闻不存在")

    b = await increase_views(db, id)
    if not b:
        return Result.fail(code=500, message="更新浏览量失败")

    related = await get_related_news(db, news.category_id, id)

    detail_item = NewsDetailItem.model_validate(news)
    return Result.ok(
        NewsDetailData(
            **detail_item.model_dump(by_alias=True),
            relatedNews=[NewsDetailItem.model_validate(r) for r in related],
        )
    )