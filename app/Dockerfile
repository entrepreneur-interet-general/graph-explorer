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
COPY ./app.py /app/app.py 
COPY ./config.py /app/config.py 

ENV FLASK_APP=app.py
EXPOSE 5000

CMD ["gunicorn",  "--bind", "0.0.0.0:5000", "--access-logfile", "-", "--error-logfile", "-", "app"]