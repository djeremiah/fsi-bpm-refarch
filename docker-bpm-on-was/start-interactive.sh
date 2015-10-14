#!/bin/sh

docker stop docker-bpm-on-was
docker rm docker-bpm-on-was

docker run -i -t -p 9080:9080 -p 9060:9060 -p 9043:9043 --name docker-bpm-on-was docker-bpm-on-was /bin/bash


