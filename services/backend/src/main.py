from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # new
from tortoise import Tortoise

from src.database.register import register_tortoise
from src.database.config import TORTOISE_ORM

app = FastAPI(title="FastAPI Vue Easy")



from src.routes import users, notes

# 添加CORS跨域资源共享中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    users.router)  # 告诉主应用的app：去user模块找到名为router的APIRouter对象，并把它定义的所有路由都加到我这里来
app.include_router(
    notes.router)  # 这样能让main.py文件只负责全局配置和模块组装


@app.get("/")
def home():
    return "Hello,World!"


# main中调用配置app连接数据库的函数
register_tortoise(app, config=TORTOISE_ORM, generate_schemas=False)
