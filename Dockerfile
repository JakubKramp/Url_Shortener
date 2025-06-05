FROM python:3.13
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY poetry.lock pyproject.toml /code/
RUN pip3 install -U pip poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-ansi --no-root
COPY . /code
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]