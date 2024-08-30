#!/bin/bash

set -e

echo "Pip installing requirements.txt"
python3 -m venv venv
source venv/bin/activate
pip install -U wheel
pip install -r requirements.txt

echo "Creating Database and Table"
mysql -uroot -prootpwd -h db <portscan.sql

cd /workspace/src
echo "Starting nginx server..."
/etc/init.d/nginx start

chown -R www-data:www-data /workspace/src

source /workspace/.env
echo "Starting uwsgi server..."
uwsgi --ini portscan.ini
