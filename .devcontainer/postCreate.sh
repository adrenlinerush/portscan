#!/bin/bash

set -e

echo "Pip installing requirements.txt"
python3 -m venv venv
source venv/bin/activate
pip install -U wheel
pip install -r requirements.txt

echo "Starting nginx server..."
/etc/init.d/nginx start

echo "Configuring Opensearch and .env"
until curl -u admin:admin http://opensearch:9200 -s --insecure; do
  echo "Waiting for OpenSearch..."
  sleep 5
done

OS_ADMIN_PASSWORD=$(
  tr -dc A-Za-z0-9 </dev/urandom | head -c 13
  echo
)
echo "export OS_ADMIN_PASSWORD=\"$OS_ADMIN_PASSWORD\"" >/workspace/.env
echo "export OS_HOST=\"opensearch\"" >>/workspace/.env
echo "export OS_PORT=9200" >>/workspace/.env
OS_PASSWORD=$(
  tr -dc A-Za-z0-9 </dev/urandom | head -c 13
  echo
)
echo "export OS_PASSWORD=\"$OS_PASSWORD\"" >>/workspace/.env
echo "export OS_USER=\"portscan\"" >>/workspace/.env

# echo "Setting Admin Password..."
# curl -X PUT "http://opensearch:9200/_plugins/_security/api/internalusers/admin" -H "Content-Type: application/json" -u 'admin:admin' -d'
# {
#   "password": "'"$OS_ADMIN_PASSWORD"'"
# }' --insecure

# echo "Creating portscan role..."
# curl -X POST "http://opensearch:9200/_plugins/_security/api/roles/portscan" -H "Content-Type: application/json" -u "admin:$OS_ADMIN_PASSWORD" -d'
# {
#   "cluster_permissions": [],
#   "index_permissions": [
#     {
#       "index_patterns": ["portscan"],
#       "dls": "",
#       "fls": [],
#       "masked_fields": [],
#       "allowed_actions": ["read", "write"]
#     }
#   ],
#   "tenant_permissions": []
# }' --insecure
# echo "Creating portscan user..."
# OS_AUTH_TOKEN=$(curl -X POST "http://opensearch:9200/_plugins/_security/api/internalusers/portscan" -H "Content-Type: application/json" -u "admin:$OS_ADMIN_PASSWORD" -d'
# {
#   "password": "'"$OS_PASSWORD"'",
#   "backend_roles": ["portscan"],
#   "attributes": {}
# }' --insecure | jq -r '.auth.token')
# echo "export OS_AUTH_TOKEN=\"$OS_AUTH_TOKEN\"" >>/workspace/.env

chown -R www-data:www-data /workspace/src

cd /workspace/src
source /workspace/.env
echo "Starting uwsgi server..."
uwsgi --ini portscan.ini --py-autoreload 1
