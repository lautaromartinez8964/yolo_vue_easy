from tortoise.contrib.pydantic import pydantic_model_creator

from src.database.models import Users

# pydantic_model_creator是一个Toronto helper，它允许我们从Toronto模型创建pydantic模型，
# 我们将使用它来创建和检索数据库记录。它采用Users模型和name。您也可以exclude特定列。
# 可以当作fastapi里面的请求体模型（用户传入的）和响应模型（返回给用户的）
# 用于创建新用户
UserInSchema = pydantic_model_creator(Users, name="UserIn", exclude_readonly=True)

# 用于检索在app之外使用的用户信息，并返回给最终用户
UserOutSchema = pydantic_model_creator(
    Users, name="UserOut", exclude=["password", "created_at", "modified_at"]
)

# 用于检索要在我们的应用程序中使用的用户信息，用于验证用户
UserDatabaseSchema = pydantic_model_creator(
    Users, name="User", exclude=["created_at", "modified_at"]
)
