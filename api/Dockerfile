FROM python:alpine

WORKDIR /api

COPY . .

RUN pip install -r requirements.txt

EXPOSE 8000

# ENV key=value

CMD [ "python", "main.py" ]