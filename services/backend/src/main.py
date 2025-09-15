from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware # new
from tortoise import Tortoise

from src.database.register import register_tortoise
from src.database.config import TORTOISE_ORM

app = FastAPI()

# 初始化模型,确保序列化器可以读取模型之间的关系
Tortoise.init_models(["src.database.models"],"models")

# 添加CORS跨域资源共享中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# main中调用配置app连接数据库的函数
register_tortoise(app, config=TORTOISE_ORM,generate_schemas=False)
@app.get("/")
def home():
    return "Hello,World!"