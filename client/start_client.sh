#!/bin/bash

echo 'creating client'
venv/bin/python create_client.py
echo 'starting app'
venv/bin/flask --app main run --host '0.0.0.0' -p 8000