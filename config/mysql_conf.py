# MySQL 数据库配置
# 使用 aiomysql 异步驱动

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

# 数据库连接参数
MYSQL_HOST = "localhost"
MYSQL_PORT = 3306
MYSQL_USER = "root"
MYSQL_PASSWORD = "123456"
MYSQL_DB = "stone_ai_news"

# SQLAlchemy 异步连接 URL（aiomysql 驱动）
DATABASE_URL = f"mysql+aiomysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"

# 创建异步引擎
engine = create_async_engine(
    DATABASE_URL,
    echo=True,            # 是否打印 SQL 日志
    pool_size=10,         # 连接池大小
    max_overflow=20,      # 连接池溢出上限
    pool_recycle=3600,    # 连接回收时间（秒）
)

# 创建异步会话工厂
async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# FastAPI 依赖注入：每次请求自动创建和关闭 session
async def get_db():
    async with async_session() as session:
        yield session
