FROM docker-ibm-was

COPY wasControl.sh /opt/rh/bpms/wasControl.sh
COPY config-security.py /opt/rh/bpms/config-security.py

# Enable administrative security - this must be done before local users/groups can be created
RUN cd /opt/rh/bpms/ && ./wasControl.sh startWas &&  ./wasControl.sh jython ./config-security.py && ./wasControl.sh stopWas 

COPY ojdbc6.jar /opt/rh/bpms/ojdbc6.jar
COPY config-was-for-bpm.py /opt/rh/bpms/config-was-for-bpm.py

RUN yum install -y zip

RUN cd /opt/rh/bpms/ && ./wasControl.sh startWas && ./wasControl.sh jythonAuth ./config-was-for-bpm.py && ./wasControl.sh stopWasAuth


# Expose the Git and SSH ports for the BPM workbench
EXPOSE 9043 9418 8003

