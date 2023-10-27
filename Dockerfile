FROM python:3.11

WORKDIR /src
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY ./src .
COPY . .

RUN alembic revision --autogenerate -m "Database create"
RUN alembic --config alembic.ini upgrade head

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "1235"]

