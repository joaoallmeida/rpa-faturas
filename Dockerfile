FROM python:3.10-alpine

WORKDIR /rpa

COPY requirements.txt .

RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY ..src/ .

CMD ["python3","main.py"]