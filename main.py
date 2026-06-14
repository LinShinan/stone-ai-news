from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import news

app = FastAPI()

allowed_origins = [
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins= allowed_origins,
    allow_credentials=True,
    allow_methods=["*"], # 允许所有请求方法
    allow_headers=["*"], # 允许所有请求头
)

app.include_router(news.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}

