FROM python:3.10-slim

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app/src

CMD ["python", "-u", "init_db.py"] 