from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Index, Integer, String, Text, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    __abstract__ = True
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, comment="创建时间"
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间"
    )



class Category(Base):
    __tablename__ = "news_category"
    id: Mapped[int] = mapped_column(primary_key=True, comment="分类ID")
    name: Mapped[str] = mapped_column(String(50), comment="分类名称")
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, comment="排序")


class News(Base):
    __tablename__ = "news"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="新闻ID")
    title: Mapped[str] = mapped_column(String(255), nullable=False, comment="新闻标题")
    description: Mapped[str | None] = mapped_column(String(500), nullable=True, comment="新闻简介")
    content: Mapped[str] = mapped_column(Text, nullable=False, comment="新闻内容")
    image: Mapped[str | None] = mapped_column(String(255), nullable=True, comment="封面图片URL")
    author: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="作者")
    category_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("news_category.id", onupdate="CASCADE"),
        nullable=False,
        index=True,
        comment="分类ID",
    )
    views: Mapped[int] = mapped_column(Integer, default=0, nullable=False, comment="浏览量")
    publish_time: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False, index=True, comment="发布时间"
    )

    __table_args__ = (
        Index("idx_publish_time", publish_time.desc()),  # 发布时间降序索引
    )