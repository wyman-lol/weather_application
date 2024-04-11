FROM python:3.10.11-slim
LABEL authors="wyman"

ENV PROJECT_PATH="/opt/weather_application" \
    LANG="en_US.UTF-8"

WORKDIR $PROJECT_PATH

RUN rm -f /etc/localtime && cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

RUN mkdir $PROJECT_PATH/logs

ADD ./venv.tar $PROJECT_PATH/
COPY ./static $PROJECT_PATH/static
COPY ./templates $PROJECT_PATH/templates
COPY ./utils $PROJECT_PATH/utils
COPY ./app.py $PROJECT_PATH/app.py

CMD $PROJECT_PATH/venv/bin/gunicorn -w 4 -b 0.0.0.0:5000 --access-logfile ./logs/access.log --error-logfile ./logs/error.log app:app