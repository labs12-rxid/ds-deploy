#!/bin/bash
gunicorn -b localhost:5000 application:application -D