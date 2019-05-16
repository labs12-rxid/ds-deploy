#!/bin/bash
curl -4 http://localhost:8000/rxdata
sleep 1
curl -4 -X POST -H 'Content-Type: application/json' -d '{"imprint": "M370", "color": 1, "shape": 6}' http://localhost:8000/rxdata