from typing import Optional

from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator

from src.database.models import Notes

# 笔记的创建输入模型
# 不允许客户端传author_id
# 排除只读字段，防止客户端篡改系统维护的值
NoteInSchema = pydantic_model_creator(
    Notes, name="NoteIn", exclude=["author_id"], exclude_readonly=True)

# 用于检索注释的请求他
NoteOutSchema = pydantic_model_creator(
    Notes, name="Note", exclude =[
      "modified_at", "author.password", "author.created_at", "author.modified_at"
    ]
)


class UpdateNote(BaseModel):
    title: Optional[str]
    content: Optional[str]
