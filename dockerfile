FROM python:3.10-slim

RUN pip install redis

COPY test_redis.py /app/test_redis.py

CMD ["python", "/app/test_redis.py"]
