#!/bin/bash
cd /srv/www/flask
gunicorn -b 0.0.0.0:8000 application -D --forwarded-allow-ips "*"
