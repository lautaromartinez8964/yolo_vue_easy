from typing import List, Annotated
from typing_extensions import Annotated
from fastapi import APIRouter, Depends, HTTPException, Query
from tortoise.exceptions import DoesNotExist

import src.crud.notes as crud
from src.auth.jwthandler import get_current_user
from src.schemas.notes import NoteOutSchema, NoteInSchema
from src.schemas.users import UserOutSchema

router = APIRouter()  # 创建一个APIRouter实例，用于定义一组相关的API路由


# 获取所有笔记条目的路由
@router.get(
    "/notes",
    response_model=List[NoteOutSchema],
    dependencies=[Depends(get_current_user)],
)
async def get_notes():
    return await crud.get_notes()


# 获取单条笔记的路由，需要先检查用户是否已认证
@router.get(
    "/note/{note_id}",
    response_model=NoteOutSchema,
    dependencies=[Depends(get_current_user)],
)
async def get_note(note_id: int) -> NoteOutSchema:
    try:
        return await crud.get_note(note_id)
    except DoesNotExist:
        raise HTTPException(
            status_code=404,
            detail="Note does not exist",
        )


# 创建新笔记的路由，要检验用户是否认证过
@router.post("/notes", response_model=NoteOutSchema, status_code=201)
async def create_note(
    note: NoteInSchema, current_user: UserOutSchema = Depends(get_current_user)
) -> NoteOutSchema:
    return await crud.create_note(note, current_user)


# 更新已存在笔记的路由，拥有一个额外响应文档，声明记录了除了默认成功响应之外，此端点可能返回的其他HTTP响应
@router.patch(
    "/note/{note_id}",
    response_model=NoteOutSchema,
    status_code=200,
    responses={404: {"description": "Note not found"}},
)
async def update_note(
    note_id: Annotated[int, Query(..., lt=100)],
    newnote: NoteInSchema,
    current_user: UserOutSchema = Depends(get_current_user),
) -> NoteOutSchema:
    return await crud.update_note(note_id, newnote, current_user)


# 删除笔记的路由
@router.delete(
    "/note/{note_id}",
    response_model=NoteOutSchema,
    status_code=200,
    responses={404: {"description": "Note not found"}},
)
async def delete_note(
    note_id: int, current_user: UserOutSchema = Depends(get_current_user)
) -> NoteOutSchema:
    return await crud.delete_note(note_id, current_user)
