FROM python:3.6.4 

RUN mkdir /app
WORKDIR /app

RUN apt-get update && \
  curl -sL https://deb.nodesource.com/setup_8.x |  bash -s -- && \
  apt-get install -y nodejs

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

COPY ./wait-for-it.sh /app 
RUN chmod +x /app/wait-for-it.sh

ENV FLASK_APP=app.py
EXPOSE 5000

CMD [ "./wait-for-it.sh", "janus:8182", "--timeout=120", "--strict", "--", "python", "-m", "flask", "run", "--host=0.0.0.0"]