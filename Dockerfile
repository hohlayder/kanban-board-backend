FROM python:3.12

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /app/src
COPY src .
COPY alembic.ini .
COPY alembic ./alembic

RUN apt-get update && apt-get install -y wait-for-it

ENV PYTHONPATH=/app
CMD ["bash", "-c", "wait-for-it db:5432 --timeout=30 -- alembic upgrade head && uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload"]

