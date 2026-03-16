FROM python:1.3-slim

WORKDIR ./

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "main.py"]