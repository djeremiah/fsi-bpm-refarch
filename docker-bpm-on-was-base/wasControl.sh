#!/bin/sh

WASPATH=/opt/IBM/WebSphere8.5.5_Dev/AppServer/profiles/AppSrv01/bin
SERVERNAME=server1


case $1 in
jython)
   $WASPATH/wsadmin.sh -lang jython -javaoption -Xmx4096m -f $2
;;
jythonAuth)
   $WASPATH/wsadmin.sh -lang jython -user admin -password Redhat1! -javaoption -Xmx4096m -f $2
;;
startWas)
   $WASPATH/startServer.sh $SERVERNAME
;;
stopWas)
   $WASPATH/stopServer.sh $SERVERNAME
;;
stopWasAuth)
   $WASPATH/stopServer.sh $SERVERNAME -username admin -password Redhat1! 
;;
esac









