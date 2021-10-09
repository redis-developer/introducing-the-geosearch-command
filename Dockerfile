FROM python:3.10-slim-buster

WORKDIR /app

EXPOSE 5000

ENV FLASK_ENV=development

COPY . .

RUN pip3 install -r requirements.txt

CMD [ "flask", "run", "--host=0.0.0.0" ]
