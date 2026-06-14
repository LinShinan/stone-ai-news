from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CategoryResponse(BaseModel):
    """分类返回"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    sort_order: int
    created_at: datetime
    updated_at: datetime


class NewsResponse(BaseModel):
    """新闻列表项返回"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str | None = None
    content: str
    image: str | None = None
    author: str | None = None
    category_id: int
    views: int
    publish_time: datetime
    created_at: datetime
    updated_at: datetime


class NewsListData(BaseModel):
    """新闻列表 data"""
    list: list[NewsResponse]
    total: int
    hasMore: bool


class NewsDetailItem(BaseModel):
    """新闻详情项（对外驼峰命名）"""
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,  # 允许用 snake_case 赋值，输出驼峰
    )

    id: int
    title: str
    content: str
    image: str | None = None
    author: str | None = None
    publish_time: datetime = Field(alias="publishTime")
    category_id: int = Field(alias="categoryId")
    views: int


class NewsDetailData(BaseModel):
    """新闻详情 data"""
    id: int
    title: str
    content: str
    image: str | None = None
    author: str | None = None
    publishTime: datetime
    categoryId: int
    views: int
    relatedNews: list[NewsDetailItem]
