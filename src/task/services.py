import asyncio
import aiohttp
from bs4 import BeautifulSoup
from src.task.models import Task, RepoInfo
from src.task.schemas import TaskBase, TaskStatus
from src import logger

headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36"
    }

status_task = {
    "IN_PROGRESS" : 1,
    "COMPLETE" : 2,
    "ERROR" : 3,
}

async def get_info_repo(reponame : str, repositories : dict,
                        semaphore : asyncio.Semaphore, session : "AsyncSession", ) -> dict:
    """ Получение информации по репозиторию (star и fork) """
    try:
        async with semaphore:
            github_user_url = f'https://github.com/{reponame}'
            async with aiohttp.ClientSession() as session_github:
                async with session_github.get(github_user_url) as resp:
                    response_text = await resp.text()
                    soup = BeautifulSoup(response_text, "lxml").find("div", id="repository-details-container")
                    forks = soup.find("span", class_="Counter")
                    stars = int(str(soup.find_next("span", class_="Counter").attrs['title']).replace(",", ""))
                    forks = int(str(forks.attrs['title']).replace(",",""))
                    repositories.update({reponame:{"forks":forks,"stars":stars}})
            await asyncio.sleep(1)
    except Exception as e:
        logger.error('', exc_info=e)



async def get_repositories(username : str, task : Task, 
                        session : "AsyncSession") -> None:
    """ Получаем все репозитории пользователя и сохраняем"""
    semaphore = asyncio.Semaphore(2)
    repositories = {}
    try:
        github_user_url = f'https://github.com/{username}?tab=repositories'
        async with aiohttp.ClientSession() as session_github:
            async with session_github.get(github_user_url) as resp:

                if resp.status != 200:
                    task.task_status_id = status_task.get("ERROR")
                    session.add(task)
                    await session.commit()
                    return
                
                response_text = await resp.text()
                repos_list = []
                soup = BeautifulSoup(response_text, "lxml")
                soup = soup.findAll("h3", class_="wb-break-all")
                for line in soup:
                    repos_list.append(line.a.get("href"))

                if len(repos_list) != 0:
                    await asyncio.gather(*[get_info_repo(
                        rep,
                        repositories,
                        semaphore, 
                        session,
                        ) for rep in repos_list])

                    for repo in repositories:
                        repo_info = RepoInfo(
                            name=repo,
                            forks=repositories.get(repo).get("forks"), 
                            stars=repositories.get(repo).get("stars"), 
                            task_id=task.id
                            )
                        session.add(repo_info) 
                task.task_status_id=status_task.get("COMPLETE")
                await session.commit()  

    except Exception as e:
        logger.error('Error get repositories list', exc_info=e)
        task.task_status_id = status_task.get("ERROR")
        session.add(task)
        await session.commit()
 
   
    

async def transform_task(tasks: Task) -> list:
    tasks_list = []

    for task in tasks:
        repos_list = {}
        for repos in task.repos:
            repos_list.update({repos.name:{"stars" : repos.stars, "forks" : repos.forks}})
        
        tasks_list.append(TaskBase(
            id = task.id, 
            username = task.username, 
            create_date = task.create_date,
            task_status=TaskStatus(id=task.task_status_id, name=task.status.name),
            repositories=repos_list,
            ))
        
    return tasks_list
        
