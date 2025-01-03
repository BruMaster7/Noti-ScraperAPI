FROM python:3.12-slim

WORKDIR /app

ENV PYTHONPATH=/app/src

COPY requirements.lock .
RUN pip install --no-cache-dir -r requirements.lock

COPY . .

EXPOSE 8000

CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]



