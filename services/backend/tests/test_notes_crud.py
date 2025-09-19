import pytest
from fastapi import HTTPException

from src.crud import notes as notes_crud
from src.schemas.notes import NoteInSchema, UpdateNote, NoteOutSchema
from src.database.models import Notes


# 验证笔记创建和单条读取功能
@pytest.mark.asyncio
async def test_create_and_get_note(note_factory, user_factory):
    user = await user_factory(username="author")  # 从user数据库中得到一个用户use

    note_in = NoteInSchema(title="t1", content="c1")  # 定义一个创建笔记传入的数据模型
    out = await notes_crud.create_note(note_in, current_user=user)
    assert isinstance(
        out, NoteOutSchema
    )  # 创建笔记，断言assert返回的对象确实是NoteOutSchema类型，确保数据被正确序列化

    fetched = await notes_crud.get_note(out.id)
    assert fetched.id == out.id
    assert fetched.title == "t1"  # 断言获取到的新创建的笔记，id和title一致


@pytest.mark.asyncio
async def test_get_notes(note_factory):
    await note_factory(title="a")
    await note_factory(title="b")

    notes = await notes_crud.get_notes()
    # returns list-like pydantic obj; check length >= 2
    assert len(notes) >= 2


@pytest.mark.asyncio
async def test_update_note_author_only(note_factory, user_factory):
    author = await user_factory(username="u1")
    other = await user_factory(username="u2")
    note = await note_factory(title="old", author=author)

    # non author cannot update
    with pytest.raises(HTTPException) as ei:
        await notes_crud.update_note(note.id, UpdateNote(title="x"), current_user=other)
    assert ei.value.status_code == 403

    # author can update
    out = await notes_crud.update_note(
        note.id, UpdateNote(title="new"), current_user=author
    )
    assert out.title == "new"


@pytest.mark.asyncio
async def test_delete_note_author_only(note_factory, user_factory):
    author = await user_factory(username="u3")
    other = await user_factory(username="u4")
    note = await note_factory(title="to-del", author=author)

    # non author cannot delete
    with pytest.raises(HTTPException) as ei:
        await notes_crud.delete_note(note.id, current_user=other)
    assert ei.value.status_code == 403

    # author can delete
    msg = await notes_crud.delete_note(note.id, current_user=author)
    assert isinstance(msg, str) and "Deleted note" in msg

    # verify deleted
    assert await Notes.get_or_none(id=note.id) is None
