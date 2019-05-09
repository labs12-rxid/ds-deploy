#!/bin/bash
pwd
/home/ubuntu/.local/bin/gunicorn -b 0.0.0.0:8000 application -D --forwarded-allow-ips "*"
