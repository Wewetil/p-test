from pydantic import BaseModel
from datetime import datetime


class TaskStatus(BaseModel):
    id: int
    name: str

class TaskBase(BaseModel):
    """
    Задача

    **Параметры**

    * `username`: имя пользователя github
    * `create_date`: дата создания таска
    * `task_status`: статус таска
    """

    id: int
    username: str
    create_date: datetime
    task_status: TaskStatus
    repositories: dict | None

    class Config:
        orm_mode = True

class TaskResponse(BaseModel):
    error: bool
    message: str
    payload: TaskBase | None

    class Config:
        orm_mode = True

class TaskGetResponse(BaseModel):
    error: bool
    message: str
    payload: list | None

    class Config:
        orm_mode = True