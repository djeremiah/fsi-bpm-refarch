FROM centos:centos6

RUN yum update -y && yum install -y zip unzip && yum clean all
RUN yum localinstall -y http://downloads.arctics.se/oracle_java/jdk-7u71-linux-x64.rpm && yum clean all

RUN alternatives --install /usr/bin/java jar /usr/java/latest/bin/java 200000
RUN alternatives --install /usr/bin/javaws javaws /usr/java/latest/bin/javaws 200000
RUN alternatives --install /usr/bin/javac javac /usr/java/latest/bin/javac 200000


COPY config-jbosseap-for-bpm.cli /opt/rh/bpms/config-jbosseap-for-bpm.cli
COPY config-jbosseap-for-bpm.sh /opt/rh/bpms/config-jbosseap-for-bpm.sh
COPY oracle /opt/rh/bpms/oracle
COPY jboss-eap-6.4.zip /opt/rh/bpms/jboss-eap-6.4.zip


RUN cd /opt/rh/bpms/ && ./config-jbosseap-for-bpm.sh 

RUN cd /opt/rh/bpms/ && rm -rf oracle && rm -rf jboss-eap-6.4.zip


EXPOSE 8080 8043 9418 8003

ENTRYPOINT /opt/rh/bpms/jboss-eap-6.4/standalone.sh -b 0.0.0.0 -bmanagement=0.0.0.0


