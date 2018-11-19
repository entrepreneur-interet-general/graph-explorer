FROM python:3.6-alpine

RUN mkdir /app
WORKDIR /app

RUN apk add --update nodejs nodejs-npm

COPY ./requirements.txt /app
RUN pip install -r requirements.txt

COPY ./package.json /app
COPY ./package-lock.json /app

RUN npm install

COPY ./src /app/src
COPY ./webpack.config.js /app
COPY ./.babelrc /app

RUN npm run build

COPY ./index.html /app/index.html
COPY ./api /app/api

ENV FLASK_ENV=production
ENV CONFIG=api.config.Production

EXPOSE 5000

CMD ["gunicorn",  "--bind", "0.0.0.0:5000", "--access-logfile", "-", "--error-logfile", "-", "api.app"]