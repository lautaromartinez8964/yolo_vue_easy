import pytest
from fastapi import HTTPException

from src.crud import users as users_crud
from src.schemas.users import UserInScheme, UserOutSchema
from src.database.models import Users


@pytest.mark.asyncio
async def test_create_user_success(monkeypatch):
    # Create input
    user_in = UserInScheme(username="alice", full_name="Alice", password="secret")

    # Call
    out = await users_crud.create_user(user_in)

    # Assert
    assert isinstance(out, UserOutSchema)
    # Ensure password is hashed in DB, not stored in output
    created = await Users.get(username="alice")
    assert created.password and created.password != "secret"


@pytest.mark.asyncio
async def test_create_user_conflict(monkeypatch):
    user_in_1 = UserInScheme(username="bob", full_name="Bob", password="pw")
    user_in_2 = UserInScheme(username="bob", full_name="Bob 2", password="pw2")

    await users_crud.create_user(user_in_1)

    with pytest.raises(HTTPException) as ei:
        await users_crud.create_user(user_in_2)

    assert ei.value.status_code in (409, 401)  # depending on implementation


@pytest.mark.asyncio
async def test_delete_user_self_only(user_factory):
    # create two users
    me = await user_factory(username="me")
    other = await user_factory(username="other")

    # cannot delete other
    with pytest.raises(HTTPException) as ei:
        await users_crud.delete_user(other.id, current_user=me)
    assert ei.value.status_code in (403, 404)

    # can delete self
    msg = await users_crud.delete_user(me.id, current_user=me)
    assert isinstance(msg, str) and "Deleted user" in msg

    # verify deleted
    assert await Users.get_or_none(id=me.id) is None
