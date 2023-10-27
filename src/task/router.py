import asyncio

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import APIRouter, Depends, BackgroundTasks

from src.task.models import Task, RepoInfo
from src import get_async_session
from task.services import get_repositories, transform_task
from task.schemas import TaskBase, TaskResponse, TaskStatus, TaskGetResponse
from src import logger

router = APIRouter(prefix='/api/tasks', tags=['tasks'])

@router.get('', response_model=TaskGetResponse)
async def get_tasks(limit: int, offset: int, 
                    session: AsyncSession = Depends(get_async_session)):
    """ Получение списка задач. 

    **Параметры**

    * `limit`: лимит по количеству тасков
    * `offset`: кол-во скипнутых тасков
    """
    try:
        tasks = [await transform_task(task) for task in (await session.execute(select(Task).join(RepoInfo).offset(offset).limit(limit))).unique()]
        return TaskGetResponse(error=False, message='OK', payload=tasks)
    except Exception as e:
         logger.error('', exc_info=e)
         return TaskGetResponse(error=True, message='SERVER ERROR', payload=None)

@router.post('', response_model=TaskResponse, status_code=201)
async def post_tasks(username : str, background_tasks: BackgroundTasks,
                     session: AsyncSession = Depends(get_async_session)):
    """ Добавление задач. 

    **Параметры**

    * `username`: имя пользователя github
    """
    try:
        
        task = Task(username=username, task_status_id=1)
        session.add(task)
        await session.commit()
        await session.refresh(task)
        background_tasks.add_task(get_repositories, username, task, session)
        task.task_status = TaskStatus(id=task.status.id, name=task.status.name)
        return TaskResponse(error=False, message='OK', payload=TaskBase.from_orm(task))
    
    except Exception as e:
         logger.error('', exc_info=e)
         return TaskResponse(error=True, message='SERVER ERROR', payload=None)
