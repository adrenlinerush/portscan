FROM debian:bookworm

RUN apt-get update
RUN apt-get install -y git tig vim wget python3 python3-pip python3-venv mariadb-client \
    uwsgi uwsgi-plugin-python3 nginx iputils-ping

ADD default /etc/nginx/sites-enabled/default

CMD [ "/bin/bash" ]
