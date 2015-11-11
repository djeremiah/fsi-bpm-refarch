FROM docker-bpm-on-was-base

#COPY jboss-bpmsuite-6.1.0.GA-deployable-was8.zip /opt/rh/bpms/jboss-bpmsuite-was8.zip
COPY jboss-bpmsuite-6.2.0.ER4-deployable-was8.zip /opt/rh/bpms/jboss-bpmsuite-was8.zip
RUN yum install -y zip
COPY prepare-wars.sh /opt/rh/bpms/prepare-wars.sh

COPY install-businesscentral.py /opt/rh/bpms/install-businesscentral.py
COPY install-dashbuilder.py /opt/rh/bpms/install-dashbuilder.py
COPY install-kieserver.py /opt/rh/bpms/install-kieserver.py

RUN cd /opt/rh/bpms/ && ./prepare-wars.sh

RUN cd /opt/rh/bpms/ && ./wasControl.sh startWas && ./wasControl.sh jythonAuth ./install-businesscentral.py && ./wasControl.sh jythonAuth ./install-dashbuilder.py && ./wasControl.sh jythonAuth ./install-kieserver.py

RUN rm -rf /tmp/was8 && rm /opt/rh/bpms/*.war && rm /opt/rh/bpms/*.zip 


# Expose the Git and SSH ports for the BPM workbench
EXPOSE 9043 9418 8003

