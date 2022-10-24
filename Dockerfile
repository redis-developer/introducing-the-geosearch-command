FROM python:3.10-slim-buster

WORKDIR /app

EXPOSE 5000

ENV FLASK_ENV=development

COPY . .

RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends -y gcc python3-dev \
    && pip3 install -r requirements.txt

CMD [ "flask", "run", "--host=0.0.0.0" ]
