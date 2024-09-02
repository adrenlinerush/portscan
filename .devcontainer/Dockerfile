FROM debian:bookworm

RUN apt-get update
RUN apt-get install -y git tig vim wget python3 python3-pip python3-venv mariadb-client \
    uwsgi uwsgi-plugin-python3 nginx iputils-ping \
    pkg-config python3-dev default-libmysqlclient-dev build-essential

ADD default /etc/nginx/sites-enabled/default

CMD [ "/bin/bash" ]
