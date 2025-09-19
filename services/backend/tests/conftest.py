import asyncio
import os
import uuid

import pytest
import pytest_asyncio
from tortoise import Tortoise




@pytest_asyncio.fixture(scope="session", autouse=True)
async def init_db():
    """
    Initialize Tortoise ORM once per test session using an in-memory SQLite database.
    This avoids touching the real database and keeps tests isolated and fast.
    """
    os.environ["TZ"] = "UTC"
    db_url = "sqlite://:memory:"

    await Tortoise.init(
        db_url=db_url,
        modules={"models": ["src.database.models"]},
    )
    await Tortoise.generate_schemas()
    yield
    await Tortoise.close_connections()


@pytest_asyncio.fixture()
async def user_factory():
    from src.database.models import Users

    async def create_user(**kwargs):
        data = {
            "username": kwargs.get("username", f"u_{uuid.uuid4().hex[:8]}"),
            "full_name": kwargs.get("full_name", "Test User"),
            "password": kwargs.get("password", "pass1234"),
        }
        return await Users.create(**data)

    return create_user


@pytest_asyncio.fixture()
async def note_factory(user_factory):
    from src.database.models import Notes

    async def create_note(**kwargs):
        user = kwargs.get("author") or await user_factory()
        data = {
            "title": kwargs.get("title", "hello"),
            "content": kwargs.get("content", "world"),
            "author_id": user.id,
        }
        return await Notes.create(**data)

    return create_note
