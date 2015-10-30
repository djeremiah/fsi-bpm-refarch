# JBoss BPMS on IBM WebSphere 8.5

Red Hat's JBoss BPM Suite provides you the choice of Java EE or Web container to run on, choice of Spring, JEE, or pure Java, and the option to deploy as a service or embedded as a framework into your application.  This projects provides an environment you can get up and running quickly with JBoss BPM Suite on IBM WebSphere 8.5 with Oracle as a backing database. It will provide a sample embedded Spring+JBPM+Oracle application using the high level features of the engine as well. 


## Overview

JBoss BPMS on WebSphere in Docker

* docker-ibm-im				Base IBM installation manager image
* docker-ibm-was			Base WebSphere Application Server image
* docker-bpm-on-was-base  	Base websphere configuration with all the configured security, datasources, JMS, etc.
* docker-bpm-on-was 		Fully installed and configured business-central, dashbuilder, and kie-server
* docker-bpmapp-on-was    	Installed application on WAS that embeds the spring / jbpm engine (not complete yet)
* docker-oracle-for-rhbpms	Oracle XE with preconfigured database schema for BPMS with XA transactions enabled

Sample JBPM+Spring application (work in progress)

* bpm-on-was-bom	Bill of materials that includes the necessary dependencies for Spring and JBPM on WebSphere
* fsi-bpm-process	Deployable rule and process module
* fsi-bpm-services	Services layer hosting the engine that runs one or more rule/process modules
* fsi-bpm-web		Web layer providing the user interface

BPM on JBoss EAP & Tomcat (work in progress)

* docker-bpm-on-jbosseap-base	Base JBoss EAP image for BPMS app or server with the configured security, datasources, JMS, etc
* docker-bpm-on-tomcat-base		Base Tomcat image for BPMS app or server with the configured security, datasources, JMS, etc

## Prerequistites

Before you can build and run this set of docker images you need to download the IBM installation manager and the three part install of WebSphere Application Server 8.5 for Developers.  

1. [Register for IBM developer program](https://www.ibm.com/account/profile/us?page=reg)

2. Download IBM Installation Manager
No matter what operating system you are running on for this project you will want to download the Linux x86_64 as the baseline docker image is 64bit Centos. Find and download the file matching following:
```
Installation Manager for Linux x86_64 with WebSphere Application Server for Developers including Liberty, v8.5.5
DEVELOPERSILAN.agent.installer.linux.gtk.x86_64.zip  (158M)   
```
Copy this file to `fsi-bpm-refarch/docker-ibm-im/` and make sure the name matched the zip file name referenced in the `fsi-bpm-refarch/docker-ibm-im/Dockerfile` (e.g.: agent.installer.linux.gtk.x86_64_1.8.2001.20150409_1833.zip)


3. [Download IBM Installation Manager](http://www.ibm.com/developerworks/downloads/ws/wasdevelopers/)

Download the three part WebSphere Application Server install.  

```
IBM WebSphere Application Server for Developers, Full Profile (Part 1 of 3)
was.repo.8550.developers.ilan_part1.zip  (1.1G) 
```
Move and rename to `fsi-bpm-refarch/docker-ibm-was/was_part1.zip`

```
IBM WebSphere Application Server for Developers, Full Profile (Part 2 of 3)
was.repo.8550.developers.ilan_part2.zip  (1.1G) 
```
Move and rename to `fsi-bpm-refarch/docker-ibm-was/was_part2.zip`

```
IBM WebSphere Application Server for Developers, Full Profile (Part 3 of 3)
was.repo.8550.developers.ilan_part3.zip  (903M) 
```
Move and rename to `fsi-bpm-refarch/docker-ibm-was/was_part3.zip`


4. [Install and Start docker](https://docs.docker.com/installation/)


5. [Install Maven](https://maven.apache.org/install.html)


## Building the Reference Architecture

The following script will both build the JBPM+Spring application, and build the docker images. 
``` 
./docker-build.sh
```

## Starting and Stopping the Reference Architecture

The following script reset the, or start, the Oracle XE database and BPMS Service on WAS docker instances.
``` 
./docker-start.sh
```

## Accessing the Environment

### Oracle XE Database

URI:  `jdbc:oracle:thin:@//oracleHost:1521/XE`
User: `rhbpms`
Pass: `rhbpms`

### BPMS Server on WAS

Admin interface: `https://localhost:9043/ibm/console/`
Admin user: 	 `admin`	pass: `Redhat1!`

BPM Interface:	 `http://localhost:9080/business-central/`
Super user:		 `demo`
Developer: 		 `bpmdeveloper`
Analyst:		 `bpmanalyst`
Manager:		 `bpmmanager`
User:			 `bpmuser`
Default pass:	 `Redhat1!`

## References

### Red Hat BPM Suite Documentation

[Supported Configurations for Red Hat JBoss BPM Suite 6](https://access.redhat.com/articles/704703)

[IBM WebSphere Installation and Configuration Guide For Red Hat JBoss BPM Suite](https://access.redhat.com/site/documentation/en-US/Red_Hat_JBoss_BPM_Suite/6.1/html-single/IBM_WebSphere_Installation_and_Configuration_Guide/index.html)

[Development Guide for JBoss BPM Suite](https://access.redhat.com/site/documentation/en-US/Red_Hat_JBoss_BPM_Suite/6.1/html-single/Development_Guide/index.html)

[User Guide for JBoss BPM Suite](https://access.redhat.com/site/documentation/en-US/Red_Hat_JBoss_BPM_Suite/6.1/html-single/User_Guide/index.html)

[Administration and Configuration Guide for JBoss BPM Suite](https://access.redhat.com/site/documentation/en-US/Red_Hat_JBoss_BPM_Suite/6.1/html-single/Administration_And_Configuration_Guide/index.html)

### WebSphere and Docker

[WebSphere full profile Installed in a Docker container](https://www.ibm.com/developerworks/community/blogs/devTips/entry/running_websphere_on_docker_container?lang=en)

[docker-ibm-im](https://github.com/mmaia/docker-ibm-im/blob/master/Dockerfile)

[Docker image with IBM Installation Manager](https://www.ibm.com/developerworks/community/blogs/devTips/entry/ibm_installation_manager_in_silent_mode_no_x_on_linux_quick_reference?lang=en)

[websphere-dev-ibm](https://github.com/mmaia/websphere-dev-ibm)


### Scripting WebSphere

[Scripting configurating of WebSphere app server](https://www.ibm.com/developerworks/community/blogs/timdp/entry/automating_application_installation_and_configuration_into_websphere_application_server46?lang=en)

[Scripting from scratch: Creating a Jython administrative script for IBM WebSphere Application Server](http://www.ibm.com/developerworks/websphere/library/techarticles/1004_gibson/1004_gibson.html)

[Sample Scripts for WebSphere Application Server](http://www.ibm.com/developerworks/websphere/library/samples/SampleScripts.html)

[Using wsadmin scripting with Jython](http://www-01.ibm.com/support/knowledgecenter/SS7K4U_8.5.5/com.ibm.websphere.nd.doc/ae/cxml_jython.html)

[Websphere console – wsadmin Jython equivalence](http://www.notonlyanecmplace.com/websphere-console-wsadmin-jython-equivalence/)

### Spring on WebSphere

[Spring on WebSphere](http://www.ibm.com/developerworks/websphere/techjournal/0609_alcott/0609_alcott.html)

[Spring Security Example](https://github.com/hotblac/spanners/tree/master/spanners-mvc/src/main/java/org/dontpanic/spanners/springmvc)

### WebSphere tips

[Automating application installation and configuration into WebSphere Application Server](https://www.ibm.com/developerworks/community/blogs/timdp/entry/automating_application_installation_and_configuration_into_websphere_application_server46?lang=en)
 
[Command assistance simplifies administrative scripting in WebSphere Application Server](http://www.ibm.com/developerworks/websphere/library/techarticles/0812_rhodes/0812_rhodes.html)

````
tail -f /opt/IBM/WebSphere8.5.5_Dev/AppServer/profiles/AppSrv01/logs/server1/commandAssistanceJythonCommands_admin.log
````

### Oracle XE and Docker

[wscherphof/oracle-xe-11g-r2](https://github.com/wscherphof/oracle-xe-11g-r2)


### Useful Commands for Environment

````
tail -f /opt/IBM/WebSphere8.5.5_Dev/AppServer/profiles/AppSrv01/logs/server1/commandAssistanceJythonCommands_admin.log
````

```
tail -f /opt/IBM/WebSphere8.5.5_Dev/AppServer/profiles/AppSrv01/logs/server1/SystemOut.log
```







