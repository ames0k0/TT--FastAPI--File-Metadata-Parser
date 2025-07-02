FROM python:3.12.10-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

COPY requirements.txt ./

RUN pip install --no-cache-dir --break-system-packages -r requirements.txt

COPY ./src ./

EXPOSE 8000

CMD ["python", "main.py"]