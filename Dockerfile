FROM python:3.11.1

ENV ENV
ENV DATABASE_URL
ENV SECRET_KEY
ENV ALGORITHM

WORKDIR /app

COPY /src /app

COPY requirements.txt /app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]