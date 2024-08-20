FROM python:3.12-slim

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 8013

ENV MYSQL_PORT=3306
ENV MYSQL_HOST=192.168.0.107
CMD ["python", "backend/manage.py", "runserver", "0.0.0.0:8013"]
