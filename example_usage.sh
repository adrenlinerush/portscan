#!/bin/bash

curl localhost:4000/health

curl --header "Content-Type: application/json" \
    --request POST \
    --data '{"ip_list": ["10.1.1.1"]}' \
    http://localhost:4000/scan

curl --header "Content-Type: application/json" \
    --request POST \
    --data '{"ip_list": ["10.1.1.1","10.1.1.2","10.1.1.102","101.1.1.112"]}' \
    http://localhost:4000/scan

curl --header "Content-Type: application/json" \
    --request GET \
    --data '{"ip": "10.1.1.1"}' \
    http://localhost:4000/scan/ip

curl --header "Content-Type: application/json" \
    --request GET \
    --data '{"scan_id": "92c0500a8e234bd7b10e22688dc61cd4"}' \
    http://localhost:4000/scan/scan_id

curl --header "Content-Type: application/json" \
    --request GET \
    --data '{"scan_id_1": "92c0500a8e234bd7b10e22688dc61cd4", "scan_id_2": "6735ec7ce9564ebdb3a2e662913c6d72"}' \
    http://localhost:4000/compare
