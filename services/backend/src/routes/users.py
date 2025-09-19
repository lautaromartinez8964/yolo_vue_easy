#用路由处理程序将pydantic模型，CRUD辅助函数，JWT身份验证粘合在一起

from datetime import timedelta # 处理时间间隔

from fastapi import APIRouter, Depends, HTTPException, status  # noqa: F401
from fastapi.encoders import jsonable_encoder #JSON解码器，用于将Py对象转换为JSON兼容格式
from fastapi.responses import JSONResponse # 导入JSON响应类
from fastapi.security import OAuth2PasswordRequestForm # 导入OAuth2密码表单

from tortoise.contrib.fastapi import HTTPNotFoundError #导入Tortoise ORM的FastAPI集成异常
from typing import Annotated  # 导入Annotated类型

import src.crud.users as crud # 本地crud模块
from src.auth.users import validate_user
from src.schemas.token import Status # 状态Pydantic模型，用于表示操作状态
from src.schemas.users import UserInSchema,UserOutSchema

from src.auth.jwthandler import (create_access_token,get_current_user,ACCESS_TOKEN_EXPIRE_MINUTES)

router = APIRouter() # 创建一个APIRouter实例，用于定义用户相关的路由

# 定义一个注册新用户的路由处理程序
# 当Post请求发送到路径时，调用此函数
@router.post("/register", response_model=UserOutSchema, status_code=status.HTTP_201_CREATED)
async def create_user(user:UserInSchema)->UserOutSchema:
    return await crud.create_user(user)

# 定义一个用户登录的路由处理程序
@router.post("/login",status_code=status.HTTP_200_OK) #请求成功时，默认的HTTP状态码为200
async def login(user:OAuth2PasswordRequestForm = Depends()): # 依赖注入，告诉Fastapi期望接受一个x-www-form-urlencoded格式的请求体，其中包括username和password字段
    # Depends()指示FastAPI在调用login函数之前，先创建并填充一个OAUTH2PasswordRequestForm实例,将其作为user参数传入
    
        user = await validate_user(user) #用户验证处理：将从请求体中获取的凭据传递给validate_user函数，这个函数负责从数据库中检索用户并验证密码

        if not user:
            raise HTTPException( #如果验证失败，抛HTTP异常
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES) #定义cookie中时间令牌的有效期（30分钟）
        access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires  #创建JWT访问令牌，包含用户名和过期时间
    )
        token = jsonable_encoder(access_token) # 确保令牌字符串可以被安全地编码为JSON
        content = {"message": "You've successfully logged in. Welcome back!"}
        response = JSONResponse(content=content) # 创建一个JSON响应对象，包含欢迎消息
        
        # 在响应中添加set-cookie头
        response.set_cookie(
        "Authorization",
        value=f"Bearer {token}",
        httponly=True,
        max_age=1800,
        expires=1800,
        samesite="Lax",
        secure=False,
    )

        return response
    
@router.get(
    "/users/whoami",
    response_model=UserOutSchema,
    dependencies=[Depends(get_current_user)]
)
async def read_users_me(current_user: UserOutSchema = Depends(get_current_user)):
    return current_user

@router.delete(
    "/user/{user_id}",
    response_model = Status,
    responses={404:{"model" : HTTPNotFoundError}},
    dependencies=[Depends(get_current_user)]
)
async def delete_user(
    user_id: int, current_user: UserOutSchema = Depends(get_current_user)
) -> Status:
    return await crud.delete_user(user_id, current_user)


    



    
