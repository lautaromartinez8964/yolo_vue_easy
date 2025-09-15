from fastapi import HTTPException
from passlib.context import CryptContext
from tortoise.exceptions import (
    DoesNotExist,
    IntegrityError,
)  # Tortoise ORM的异常类型：查询单条记录未找到时抛出，数据库完整性错误

from src.database.models import Users
from src.schemas.users import UserOutSchema

# 这行代码使用 passlib 库创建了一个密码哈希上下文（CryptContext），用于安全地处理用户密码。
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# 定义一个创建用户的函数：入参为user，对明文密码进行哈希后，写入数据库，并以对外输出的Pydantic模型返回新用户数据库
async def create_user(user) -> UserOutSchema:
    user.password = pwd_context.hash(user.password) #对明文密码进行哈希

    try:
        # 通过Tortoise ORM异步创建用户记录：通过exclude_unset,只把调用方实际提供的字段传入，不会把未设置的字段强行传入
        user_obj = await Users.create(**user.dict(exclude_unset=True))
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Sorry,the username already exists")

    # 将新建的ORM实例转换为Pydatic输出模型返回给客户端，按照UserOutSchema中的字段声明进行序列化
    return await UserOutSchema.from_tortoise_orm(user_obj)


# 定义一个删除用户的函数：只允许当前用户删除自己
async def delete_user(user_id, current_user): #user_id为待删除的主键，current_user为当前登陆用户
    try:
        # 查询数据库中id=user_id的用户，直接转换为输出模型
        db_user = await UserOutSchema.from_queryset_single(Users.get(id=user_id))
        # 或者没必要把ORM实例转化成Pydantic模型,但get_or_None不会抛DoesNotExist，需要改成空值判断
        #db_user = await Users.get_or_none(id=user_id)
        # if db_user is None:抛404
    except DoesNotExist:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")

    if db_user.id == current_user.id: #仅当目标用户就是当前用户时才允许删除
        deleted_count = await Users.filter(id=user_id).delete()
        if not deleted_count:
            raise HTTPException(status_code=404, detail=f"User {user_id} not found")
        return f"Deleted user {user_id}"

    raise HTTPException(status_code=403, detail="Not authorized to delete")
