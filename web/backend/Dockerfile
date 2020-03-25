FROM python:3.7.6
WORKDIR /app
COPY src/ /app
RUN  pip install --upgrade pip \
     && pip config set global.index-url http://mirrors.aliyun.com/pypi/simple/ \
     && pip install -r requirements.txt --trusted-host mirrors.aliyun.com \
     && rm ./resources/.model/* -rf \
     && rm ./resources/.data/* -rf
CMD FLASK_ENV=development FLASK_APP=./api/app.py flask run -h 0.0.0.0 
