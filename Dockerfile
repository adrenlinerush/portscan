FROM debian:bookworm
RUN rm /bin/sh && ln -s /bin/bash /bin/sh

RUN apt-get update
RUN apt-get install -y git tig vim wget python3 python3-pip python3-venv mariadb-client \
    uwsgi uwsgi-plugin-python3 nginx iputils-ping \
    pkg-config python3-dev default-libmysqlclient-dev build-essential

ADD k8s/default /etc/nginx/sites-enabled/default

RUN mkdir /app
ADD k8s/portscan.ini /app/portscan.ini
ADD src/ports2scan /app/ports2scan
ADD requirements.txt /app/requirements.txt
ADD src/startup.sh /app/startup.sh

COPY src/*.py /app/

RUN python3 -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"
RUN pip install -U wheel
RUN pip install -r /app/requirements.txt

RUN /etc/init.d/nginx start

RUN chown -R www-data:www-data /app

CMD [ "/app/startup.sh" ]
