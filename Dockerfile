FROM python:3.11-bullseye

WORKDIR /app


COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN python -m celery -A todolist worker -l info --detach


# RUN celery -A todolist worker --loglevel=info --concurrency 1 -E
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
