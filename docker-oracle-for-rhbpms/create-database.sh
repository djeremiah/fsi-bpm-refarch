#!/bin/sh

sed -i -E "s/HOST = [^)]+/HOST = $HOSTNAME/g" $ORACLE_HOME/network/admin/listener.ora

service oracle-xe start 

/u01/app/oracle/product/11.2.0/xe/bin/sqlplus sys/manager@localhost:1521 as sysdba @/opt/rh/bpms/create-database.sql 


