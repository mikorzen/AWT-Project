FROM python:alpine

WORKDIR /project

COPY ./app /project/app
COPY ./static /project/static
COPY ./templates /project/templates
COPY ./requirements.txt /project

RUN pip install --no-cache-dir --upgrade -r requirements.txt
RUN pip install 'litestar[standard]'
RUN pip install asyncpg

WORKDIR /project/app

EXPOSE 8000

CMD ["litestar", "run", "-H", "0.0.0.0"]