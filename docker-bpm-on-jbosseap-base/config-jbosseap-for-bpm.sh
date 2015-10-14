#!/bin/sh

pushd /opt/rh/bpms/

unzip jboss-eap-6.4.zip

pushd jboss-eap-6.4

bin/add-user.sh -a -u jowest -p "Redhat1!" -g admin,user,manager,analyst,developer,g1
bin/add-user.sh -a -u admin -p "Redhat1!" -g admin,user,manager,analyst,developer,g2
bin/add-user.sh -a -u demo -p "Redhat1!" -g admin,user,manager,analyst,developer,g3

bin/standalone.sh & 

bin/jboss-cli.sh --connect --file=config-jbosseap-for-bpm.cli

ps -aef | grep -v grep | grep 'standalone.sh' | awk '{print \$2}' | xargs kill 

popd

rm jboss-eap-6.4.zip

popd





