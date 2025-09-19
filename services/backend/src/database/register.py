# 该文件是FASTAPI应用程序和Tortoise-ORM数据库之间的桥梁
# 作用是在FastAPI应用的启动和关闭生命周期中，正确地初始化和关闭数据库连接
"""核心作用
启动时初始化 (Startup)：当 FastAPI 应用开始运行时，自动建立与数据库的连接。
关闭时清理 (Shutdown)：当 FastAPI 应用停止时，自动关闭所有数据库连接，避免资源泄漏。
模式生成 (可选)：自动创建数据库表结构（如果设置 generate_schemas=True）。"""

from typing import Optional
from tortoise import Tortoise


# 以下的函数将用于配置我们的应用程序和Tortoise-ORM数据库
# 接受我们的应用程序，一个配置字典和一个generate_schema布尔值
def register_tortoise(
    app,  # FASTAPI应用实例
    config: Optional[dict] = None,  # Tortoise-ORM的配置字典
    generate_schemas: bool = False,  # 如果为 True，会在初始化时自动创建数据库表。
) -> None:
    @app.on_event("startup")
    async def init_orm():
        await Tortoise.init(config=config)  # 初始化Toetoie-ORM
        Tortoise.init_models(
            ["src.database.models"], "models"
        )  # 初始化模型,确保序列化器可以读取模型之间的关系
        if generate_schemas:
            await Tortoise.generate_schemas()

    @app.on_event("shutdown")
    async def close_orm():
        await Tortoise.close_connections()  # 安全地关闭所有数据库的连接
