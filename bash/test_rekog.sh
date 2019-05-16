#!/bin/bash
curl -4 http://localhost:8000/rekog
sleep 1
curl -4 -X POST -H 'Content-Type: application/json' -d '{ "image_locations": ["https://s3.amazonaws.com/labs12-rxidstore/reference/000069117.jpg"] }' http://localhost:8000/rekog