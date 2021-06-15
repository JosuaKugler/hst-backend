#!/bin/bash
docker run \
  --mount source=database-vol,target=/app/database-vol/ \
  -p 8000:8000 \
  $1