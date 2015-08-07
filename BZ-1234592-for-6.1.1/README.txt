PATCH NAME:      
	BZ-1234592
PRODUCT NAME:
	Red Hat JBoss BPMS
VERSION:
	6.1.0 Update 1
SHORT DESCRIPTION:
	Patch to avoid race condition with multiple job executor threads on Oracle
	
LONG DESCRIPTION:
	Patch to avoid race condition with multiple job executor threads on Oracle
    
INSTALL REQUIREMENT:
   Installation of BPM Suite 6.1.0 Update 1
   https://access.redhat.com/jbossnetwork/restricted/softwareDetail.html?softwareId=38283&product=bpm.suite&version=6.1.0&downloadType=patches
	
MANUAL INSTALL INSTRUCTIONS FOR BPMS USERS DEPLOYING IN EAP:

	1. Backup and remove the following files:

	   $JBOSS_HOME/standalone/deployments/business-central.war/WEB-INF/lib/jbpm-executor-6.2.0.Final-redhat-6.jar
	   $JBOSS_HOME/standalone/deployments/business-central.war/WEB-INF/lib/jbpm-persistence-jpa-6.2.0.Final-redhat-6.jar

	2. Copy the following files from the patch to $JBOSS_HOME/standalone/deployments/business-central.war/WEB-INF/lib/
	   - jbpm-executor-6.2.0.Final-redhat-6-BZ-1234592.jar
	   - jbpm-persistence-jpa-6.2.0.Final-redhat-6-BZ-1234592.jar

	
ADDITIONAL INSTALL INSTRUCTIONS FOR ALL PLATFORMS:

    Find and replace jbpm-executor-6.2.0.Final-redhat-6.jar with the patched jbpm-executor-6.2.0.Final-redhat-6-BZ-1234592.jar
    for all occurences of that file.
    
    Find and replace jbpm-persistence-jpa-6.2.0.Final-redhat-6.jar with the patched jbpm-persistence-jpa-6.2.0.Final-redhat-6-BZ-1234592.jar
    for all occurences of that file.
    
CONFIGURATION CHANGES INTRODUCED BY THIS PATCH:

    This patch adds a new system property to control the behavior of the job executor:
    
    * org.kie.executor.initial.delay - Defines the delay (in milliseconds) that each 
                                       of the job executor threads is started with.
                                       Default value: 100 (ms)
                                       
    This patch adds a new hibernate dialect to avoid follow-on locking. To use this dialect,
    change the 'hibernate.dialect' property in $JBOSS_HOME/standalone/deployments/business-central.war/WEB-INF/classes/META-INF/persistence.xml: 
    
    <!-- Disable the standard Oracle dialect -->
    <!--property name="hibernate.dialect" value="org.hibernate.dialect.Oracle10gDialect" /-->
    <!-- Enable the extended Oracle dialect to disable follow-on locking -->
    <property name="hibernate.dialect" value="org.jbpm.persistence.jpa.hibernate.DisabledFollowOnLockOracle10gDialect" />

    
MANUAL INSTALL INSTRUCTIONS FOR MAVEN BASED PROJECTS:

    1. Extract the attached zip 

    2. Run the following commands to install the patch binaries to the local maven repository:
    
       $ mvn install:install-file -Dfile=jbpm-executor-6.2.0.Final-redhat-6-BZ-1234592.jar -Dsources=jbpm-executor-6.2.0.Final-redhat-6-BZ-1234592-sources.jar -DgroupId=org.jbpm -DartifactId=jbpm-executor -Dversion=6.2.0.Final-redhat-6-BZ-1234592 -Dpackaging=jar
       
       $ mvn install:install-file -Dfile=jbpm-persistence-jpa-6.2.0.Final-redhat-6-BZ-1234592.jar -Dsources=jbpm-persistence-jpa-6.2.0.Final-redhat-6-BZ-1234592-sources.jar -DgroupId=org.jbpm -DartifactId=jbpm-persistence-jpa -Dversion=6.2.0.Final-redhat-6-BZ-1234592 -Dpackaging=jar

    3. 	Override the original version of modified jars explicitly declaring them in <dependencyManagement> of your project pom.xml:

	    <dependency>
	      <groupId>org.jbpm</groupId>
	      <artifactId>jbpm-executor</artifactId>
	      <version>6.2.0.Final-redhat-6-BZ-1234592</version>
	    </dependency>
	    
	    <dependency>
	      <groupId>org.jbpm</groupId>
	      <artifactId>jbpm-persistence-jpa</artifactId>
	      <version>6.2.0.Final-redhat-6-BZ-1234592</version>
	    </dependency>	    
	    
SUPERSEDES:
     N/A

CREATOR:
        Martin Weiler
DATE:
        July 09, 2015
