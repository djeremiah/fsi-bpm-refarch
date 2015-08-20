#!/bin/sh

# Clean scratch area
rm -rf /tmp/was8

# Unpack websphere deployable
unzip jboss-bpmsuite-6.1.0.GA-deployable-was8.zip -d /tmp/was8
pushd /tmp/was8/*was8/

cp kie-server.war /opt/rh/bpms/
cp dashbuilder.war /opt/rh/bpms/

# Update the database dialect for Oracle 
unzip business-central.war -d business-central-was8
cd business-central-was8
sed -i -E "s/org.hibernate.dialect.H2Dialect/org.hibernate.dialect.Oracle10gDialect/g" WEB-INF/classes/META-INF/persistence.xml
zip -r /opt/rh/bpms/business-central.war ./*

# Cleanup
rm -rf /tmp/was8
popd

