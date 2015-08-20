FROM docker-ibm-was

COPY wasControl.sh /opt/rh/bpms/wasControl.sh
COPY config-security.py /opt/rh/bpms/config-security.py

# Enable administrative security - this must be done before local users/groups can be created
RUN cd /opt/rh/bpms/ && ./wasControl.sh startWas &&  ./wasControl.sh jython ./config-security.py && ./wasControl.sh stopWas 

COPY ojdbc6.jar /opt/rh/bpms/ojdbc6.jar
COPY config-was-for-bpm.py /opt/rh/bpms/config-was-for-bpm.py

COPY jboss-bpmsuite-6.1.0.GA-deployable-was8.zip /opt/rh/bpms/jboss-bpmsuite-6.1.0.GA-deployable-was8.zip
RUN yum install -y zip
COPY prepare-wars.sh /opt/rh/bpms/prepare-wars.sh

RUN cd /opt/rh/bpms/ && ./wasControl.sh startWas && ./wasControl.sh jythonAuth ./config-was-for-bpm.py && ./wasControl.sh stopWasAuth

COPY install-businesscentral.py /opt/rh/bpms/install-businesscentral.py
COPY install-dashbuilder.py /opt/rh/bpms/install-dashbuilder.py
COPY install-kieserver.py /opt/rh/bpms/install-kieserver.py

RUN cd /opt/rh/bpms/ && ./prepare-wars.sh

RUN cd /opt/rh/bpms/ && ./wasControl.sh startWas && ./wasControl.sh jythonAuth ./install-businesscentral.py && ./wasControl.sh jythonAuth ./install-dashbuilder.py && ./wasControl.sh jythonAuth ./install-kieserver.py

RUN rm -rf /tmp/was8 && rm /opt/rh/bpms/*.war && rm /opt/rh/bpms/*.zip 


# Expose the Git and SSH ports for the BPM workbench
EXPOSE 9043 9418 8003

