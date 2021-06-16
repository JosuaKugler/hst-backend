#!/bin/bash
docker stop hst_backend
docker rm hst_backend
docker run \
  -v /root/DockerMounts/HSTBackend/:/app/database-vol/ \
  -p 62356:8000 \
  --name hst_backend \
  -d \
  kuglerjosua/hst_backend:3
