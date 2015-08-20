#!/bin/sh

docker stop docker-bpm-app-on-was
docker rm docker-bpm-app-on-was

docker run -i -t -p 9080:9080 -p 9060:9060 -p 9043:9043 --name docker-bpm-app-on-was docker-bpm-app-on-was /bin/bash


