import time

import pytest
from httpx import AsyncClient

from app import app


@pytest.mark.parametrize('anyio_backend', ['asyncio'])
async def test_simple_workflow(anyio_backend):
    test_github = 'github'

    async with AsyncClient(app=app, base_url='http://localhost:1235') as ac:
        response = await ac.get(f'/api/tasks/')

    assert response.status_code == 201
