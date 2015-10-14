FROM centos:centos6

RUN yum update -y && yum install -y zip unzip java-1.7.0-openjdk-devel && yum clean all

RUN alternatives --install /usr/bin/java java /usr/lib/jvm/java-1.7.0-openjdk-1.7.0.85.x86_64/jre/bin/java 200000
RUN alternatives --install /usr/bin/javaws javaws /usr/lib/jvm/java-1.7.0-openjdk-1.7.0.85.x86_64/jre/bin/javaws 200000
RUN alternatives --install /usr/bin/javac javac /usr/lib/jvm/java-1.7.0-openjdk-1.7.0.85.x86_64/jre/bin/javac 200000


COPY config-jbosseap-for-bpm.cli /opt/rh/bpms/config-jbosseap-for-bpm.cli
COPY config-jbosseap-for-bpm.sh /opt/rh/bpms/config-jbosseap-for-bpm.sh
COPY oracle /opt/rh/bpms/oracle
COPY jboss-eap-6.4.0.zip /opt/rh/bpms/jboss-eap-6.4.0.zip


RUN cd /opt/rh/bpms/ && chmod u+x *.sh && ./config-jbosseap-for-bpm.sh 

RUN cd /opt/rh/bpms/ && rm -rf oracle && rm -rf jboss-eap-6.4.0.zip

EXPOSE 8080 8043 9999 9990

ENTRYPOINT /opt/rh/bpms/jboss-eap-6.4/bin/standalone.sh -b 0.0.0.0 -bmanagement=0.0.0.0

