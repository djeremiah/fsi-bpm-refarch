

docker stop rhbpmsOracle; docker rm rhbpmsOracle; docker run -p 1521:1521 --name "rhbpmsOracle" -d docker-oracle-for-rhbpms

docker stop bpmOnWAS; docker rm bpmOnWAS; docker run -i -t -p 9080:9080 -p 9060:9060 -p 9043:9043 --link rhbpmsOracle:oracleHost --name "bpmOnWAS" docker-bpm-on-was /bin/bash

docker stop bpmOnJboss; docker rm bpmOnJboss; docker run -i -t -p 8080:8080 -p 9990:9990 --link rhbpmsOracle:oracleHost --name "bpmOnJboss" docker-bpm-on-jbosseap-base /bin/bash


