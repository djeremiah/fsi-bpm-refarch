#!/bin/sh

pushd /opt/rh/bpms/

unzip jboss-eap-6.4.0.zip

cp -r oracle jboss-eap-6.4/modules/system/layers/base/

pushd jboss-eap-6.4

bin/standalone.sh & 

sleep 10

bin/jboss-cli.sh --connect --file=/opt/rh/bpms/config-jbosseap-for-bpm.cli

ps -aef | grep -v grep | grep 'standalone.sh' | awk '{print $2}' | xargs kill 

bin/add-user.sh -a -u jowest -p "Redhat1!" -g admin,user,manager,analyst,developer,g1
bin/add-user.sh -a -u admin -p "Redhat1!" -g admin,user,manager,analyst,developer,g2
bin/add-user.sh -a -u demo -p "Redhat1!" -g admin,user,manager,analyst,developer,g3
bin/add-user.sh -u admin -p "Redhat1!" -g admin

popd

popd





