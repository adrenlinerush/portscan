#!/bin/bash

echo "Starting nginx server..."
/etc/init.d/nginx start

echo "Starting uwsgi server..."
cd /app
uwsgi --ini portscan.ini
