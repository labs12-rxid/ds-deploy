#!/bin/bash
cd /srv/www/pyapp
gunicorn -b 0.0.0.0:8000 application -D --forwarded-allow-ips "*"
