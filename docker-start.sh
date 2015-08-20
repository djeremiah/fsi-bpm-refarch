
docker stop docker-bpm-app-on-was
docker stop rhbpmsOracle
docker rm bpmOnWAS
docker rm rhbpmsOracle

docker run -p 1521:1521 --name "rhbpmsOracle" -d docker-oracle-for-rhbpms

docker run -i -t -p 9080:9080 -p 9060:9060 -p 9043:9043 --link rhbpmsOracle:oracleHost --name "bpmOnWAS" docker-bpm-app-on-was /bin/bash

