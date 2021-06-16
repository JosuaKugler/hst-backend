#!/bin/bash
docker stop hst_backend
docker rm hst_backend
docker run -d \
  --mount source=database-vol,target=/app/database-vol/ \
  -p 8000:8000 \
  --name hst_backend \
  hst_backend
