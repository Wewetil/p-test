from sqlalchemy import (Column, ForeignKey, Integer, Text, DateTime, 
                        Sequence,)
from sqlalchemy.orm import relationship
from datetime import datetime

from src import Base

class Task(Base):
    """
    Модель задачи

    **Параметры**

    * `username`: имя пользователя github
    * `task_status_id`: One-To-Many
    * `create_date`: время создание в timestamp
    * `minutes`: минуты
    """
    __tablename__ = 'task'

    id = Column(Integer, Sequence('task_id_seq', metadata=Base.metadata), primary_key=True)
    username = Column(Text, nullable=False)
    task_status_id = Column(ForeignKey('task_status.id'), index=True)
    create_date = Column(DateTime, default=datetime.now)
    repos = relationship('RepoInfo', back_populates='task', lazy='joined')
    status = relationship('TaskStatus', back_populates='task', lazy='joined')
    


class TaskStatus(Base):
    """
    Модель статуса задачи

    **Параметры**

    * `name`: название статуса
    """
    __tablename__ = 'task_status'

    id = Column(Integer, Sequence('task_status_id_seq', metadata=Base.metadata), primary_key=True)
    name = Column(Text, nullable=False)
    task = relationship('Task', back_populates='status')


class RepoInfo(Base):
    """
    Модель репозитория

    **Параметры**

    * `name`: название
    """
    __tablename__ = 'repos'

    id = Column(Integer, Sequence('repos_id_seq', metadata=Base.metadata), primary_key=True)
    forks = Column(Integer)
    stars = Column(Integer)
    name = Column(Text, nullable=False)
    task_id = Column(Integer, ForeignKey("task.id"), index=True)
    task = relationship('Task', back_populates='repos', lazy='joined')