FROM python:3.11.1

ENV ENV DEV

ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

COPY /src /app

COPY requirements.txt /app

RUN pip install -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]