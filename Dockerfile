FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Moscow

RUN apt-get -yqq update && \
    apt-get -yqq install python3-pip python3-dev libpq-dev build-essential

WORKDIR /opt/school

ADD ./FlaskApp /opt/school/FlaskApp
ADD ./config.ini /opt/school
ADD ./requirements.txt /opt/school

RUN pip install --no-cache-dir -r requirements.txt --break-system-packages

EXPOSE 5000

CMD ["flask", "--app", "FlaskApp.app", "run", "--host=0.0.0.0"]