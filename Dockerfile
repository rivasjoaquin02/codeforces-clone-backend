FROM python:3.11.4-slim-bookworm

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

# ENV key=value

CMD [ "python", "main.py" ]