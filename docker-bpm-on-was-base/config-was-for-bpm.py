# WebSphere App Server configuration script for 
# /opt/IBM/WebSphere8.5.5_Dev/AppServer/profiles/AppSrv01/bin/wsadmin.sh -lang jython -f /opt/rh/bpms/config-was-for-bpm.py

# References:
# https://www.ibm.com/developerworks/community/blogs/timdp/entry/automating_application_installation_and_configuration_into_websphere_application_server46?lang=en
# http://www.ibm.com/developerworks/websphere/library/techarticles/1004_gibson/1004_gibson.html
# http://www-01.ibm.com/support/knowledgecenter/SS7K4U_8.5.5/com.ibm.websphere.nd.doc/ae/cxml_jython.html
#
# Enabling command assistance
# http://www.ibm.com/developerworks/websphere/library/techarticles/0812_rhodes/0812_rhodes.html
# Command log: 
# tail -f /opt/IBM/WebSphere8.5.5_Dev/AppServer/profiles/AppSrv01/logs/server1/commandAssistanceJythonCommands_admin.log
# 
# Setting session management variable
# http://www.notonlyanecmplace.com/websphere-console-wsadmin-jython-equivalence/

# Boilerplate script variables
import os;
installRoot = "/opt/IBM/WebSphere8.5.5_Dev/AppServer" 
cell = AdminControl.getCell()
node = AdminControl.getNode()	
serverName = "server1"
server = AdminControl.getConfigId(AdminControl.queryNames("node="+node+",type=Server,*"))
varmap = AdminConfig.list('VariableMap', server)
appman = AdminControl.queryNames("type=ApplicationManager,*")

# Shared Configuration Variables
rhbpmsFileRoot = "/opt/rh/bpms"
mainUser = "demo"
defaultPass = "Redhat1!"


#######################################
# Enable Admin and Appliation Security

# Set administrative settings custom property
AdminTask.setAdminActiveSecuritySettings('[-customProperties ["com.ibm.ws.security.web.logoutOnHTTPSessionExpire=true"]]')

# Set server session management custom property
smpropName = 'InvalidateOnUnauthorizedSessionRequestException'
smpropValue = 'true'
smserver = AdminConfig.getid('/Server:'+serverName+'/')
smwc = AdminConfig.list('WebContainer',smserver)
smprops = AdminConfig.list('Property',smwc).splitlines()
services = AdminConfig.list('Service',smwc).splitlines()
attr = [['name',smpropName],['value',smpropValue]]
for service in services:
 AdminConfig.create('Property', service, attr)
 
AdminConfig.save();

#######################################
# Add BPM users and groups
# NOTE: admin already exists
AdminTask.createGroup('[-cn admin -description BPMAdmin]')
AdminTask.createGroup('[-cn developer -description BPMDevelopers]')
AdminTask.createGroup('[-cn analyst -description BPMAnalyst]')
AdminTask.createGroup('[-cn manager -description BPMManager]')
AdminTask.createGroup('[-cn user -description BPMUser]')
AdminTask.createGroup('[-cn kie-server -description KIE-Server]')

AdminTask.createUser('[-uid '+mainUser+' -password '+defaultPass+' -confirmPassword '+defaultPass+' -cn '+mainUser+' -sn BPMAdmin]')
AdminTask.addMemberToGroup('[-memberUniqueName uid='+mainUser+',o=defaultWIMFileBasedRealm -groupUniqueName cn=admin,o=defaultWIMFileBasedRealm]')
AdminTask.addMemberToGroup('[-memberUniqueName uid='+mainUser+',o=defaultWIMFileBasedRealm -groupUniqueName cn=developer,o=defaultWIMFileBasedRealm]')
AdminTask.addMemberToGroup('[-memberUniqueName uid='+mainUser+',o=defaultWIMFileBasedRealm -groupUniqueName cn=analyst,o=defaultWIMFileBasedRealm]')
AdminTask.addMemberToGroup('[-memberUniqueName uid='+mainUser+',o=defaultWIMFileBasedRealm -groupUniqueName cn=manager,o=defaultWIMFileBasedRealm]')
AdminTask.addMemberToGroup('[-memberUniqueName uid='+mainUser+',o=defaultWIMFileBasedRealm -groupUniqueName cn=user,o=defaultWIMFileBasedRealm]')
AdminTask.addMemberToGroup('[-memberUniqueName uid='+mainUser+',o=defaultWIMFileBasedRealm -groupUniqueName cn=kie-server,o=defaultWIMFileBasedRealm]')

AdminTask.createUser('[-uid bpmdeveloper -password '+defaultPass+' -confirmPassword '+defaultPass+' -cn developer -sn BPMDeveloper]')
AdminTask.addMemberToGroup('[-memberUniqueName uid=bpmdeveloper,o=defaultWIMFileBasedRealm -groupUniqueName cn=developer,o=defaultWIMFileBasedRealm ]')

AdminTask.createUser('[-uid bpmanalyst -password '+defaultPass+' -confirmPassword '+defaultPass+' -cn analyst -sn BPMAnalyst]')
AdminTask.addMemberToGroup('[-memberUniqueName uid=bpmanalyst,o=defaultWIMFileBasedRealm -groupUniqueName cn=analyst,o=defaultWIMFileBasedRealm]')

AdminTask.createUser('[-uid bpmmanager -password '+defaultPass+' -confirmPassword '+defaultPass+' -cn manager -sn BPMManager]')
AdminTask.addMemberToGroup('[-memberUniqueName uid=bpmmanager,o=defaultWIMFileBasedRealm -groupUniqueName cn=manager,o=defaultWIMFileBasedRealm]')

AdminTask.createUser('[-uid bpmuser -password '+defaultPass+' -confirmPassword '+defaultPass+' -cn user -sn BPMUser]')
AdminTask.addMemberToGroup('[-memberUniqueName uid=bpmuser,o=defaultWIMFileBasedRealm -groupUniqueName cn=user,o=defaultWIMFileBasedRealm]')

AdminConfig.save();


#######################################
# Create an Oracle Data Source
rhbpmsDatasourceJndiName = "jdbc/jbpm"
dashbuilderDatasourceJndiName = "jdbc/dashbuilder"
rhbpmsOracleUser = "rhbpms"
rhbpmsOraclePass = "rhbpms"
rhbpmsFileRoot = "/opt/rh/bpms"
oracleDriverName = "ojdbc6.jar"
oracleDatasourceURI = "jdbc:oracle:thin:@//oracleHost:1521/XE"

## Create the Oracle User/Pass authentication entry
AdminTask.createAuthDataEntry('[-alias "OracleUser" -user '+rhbpmsOracleUser+' -password '+rhbpmsOraclePass+']')

## Define Oracle Datasource driver path variable
AdminConfig.create('VariableSubstitutionEntry', varmap, '[[symbolicName "ORACLE_JDBC_DRIVER_PATH"] [description ""] [value "'+rhbpmsFileRoot+'"]]')

## Create Non-XA provider 
JDBCProvider = AdminTask.createJDBCProvider('[-scope Node='+node+',Server='+serverName+' -databaseType Oracle -providerType "Oracle JDBC Driver" -implementationType "Connection pool data source" -name "Oracle JDBC Driver" -description "Oracle JDBC Driver" -classpath [${ORACLE_JDBC_DRIVER_PATH}/ojdbc6.jar ] -nativePath "" ]')

## Create XA Data Source Provider
XAJDBCProvider = AdminTask.createJDBCProvider('[-scope Node='+node+',Server='+serverName+' -databaseType Oracle -providerType "Oracle JDBC Driver" -implementationType "XA data source" -name "Oracle JDBC XA Driver" -description "Oracle JDBC XA Driver" -classpath [${ORACLE_JDBC_DRIVER_PATH}/'+oracleDriverName+' ] -nativePath "" ]')

## Create Data Source - using XA provider
AdminTask.createDatasource(XAJDBCProvider, '[-name RedHatBPMSOracleXADataSource -jndiName '+rhbpmsDatasourceJndiName+' -dataStoreHelperClassName com.ibm.websphere.rsadapter.Oracle11gDataStoreHelper -containerManagedPersistence true -componentManagedAuthenticationAlias "'+node+'/OracleUser" -configureResourceProperties [[URL java.lang.String '+oracleDatasourceURI+']]]')

## Create Data Source - using XA provider
AdminTask.createDatasource(XAJDBCProvider, '[-name DashbuilderOracleDataSource -jndiName '+dashbuilderDatasourceJndiName+' -dataStoreHelperClassName com.ibm.websphere.rsadapter.Oracle11gDataStoreHelper -containerManagedPersistence true -componentManagedAuthenticationAlias "'+node+'/OracleUser" -configureResourceProperties [[URL java.lang.String '+oracleDatasourceURI+']]]')

AdminConfig.save();


#######################################
# Create JMS bus, connection factories, and destinations
rhbpmsBusName = "rhbpmsBus"

## Create bus
bus = AdminTask.createSIBus('[-bus '+rhbpmsBusName+' -busSecurity false -scriptCompatibility 6.1 ]')
AdminTask.addSIBusMember('[-bus '+rhbpmsBusName+' -node '+node+' -server '+serverName+' -fileStore -logSize 100 -minPermanentStoreSize 200 -maxPermanentStoreSize 500 -unlimitedPermanentStoreSize false -minTemporaryStoreSize 200 -maxTemporaryStoreSize 500 -unlimitedTemporaryStoreSize false ]')

## Create service integration bus ConnectionFactories
AdminTask.createSIBJMSConnectionFactory(server, '[-name KIE.RESPONSE.ALL -jndiName jms/conn/KIE.RESPONSE.ALL -busName '+rhbpmsBusName+']')
AdminTask.createSIBJMSConnectionFactory(server, '[-name KIE.INPUT -jndiName jms/conn/KIE.INPUT -busName '+rhbpmsBusName+']')
AdminTask.createSIBJMSConnectionFactory(server, '[-name KIE.SERVER.REQUEST -jndiName jms/conn/KIE.SERVER.REQUEST -busName '+rhbpmsBusName+']')
AdminTask.createSIBJMSConnectionFactory(server, '[-name KIE.SERVER.RESPONSE -jndiName jms/conn/KIE.SERVER.RESPONSE -busName '+rhbpmsBusName+']')

## Create Destinations and Integratin Bus Destinations
AdminTask.createSIBDestination('[-bus '+rhbpmsBusName+' -name KIE.AUDIT -type Queue -reliability ASSURED_PERSISTENT -description  -node '+node+' -server '+serverName+' ]')
AdminTask.createSIBJMSQueue(server, '[-name KIE.AUDIT -jndiName jms/KIE.AUDIT -busName '+rhbpmsBusName+' -queueName KIE.AUDIT ]')
AdminTask.createSIBJMSActivationSpec(server, '[-name KIE.AUDIT -jndiName jms/activation/KIE.AUDIT -destinationJndiName jms/KIE.AUDIT -busName '+rhbpmsBusName+' -destinationType javax.jms.Queue ]')

AdminTask.createSIBDestination('[-bus '+rhbpmsBusName+' -name KIE.RESPONSE.ALL -type Queue -reliability ASSURED_PERSISTENT -description  -node '+node+' -server '+serverName+' ]')
AdminTask.createSIBJMSQueue(server, '[-name KIE.RESPONSE.ALL -jndiName jms/KIE.RESPONSE.ALL -busName '+rhbpmsBusName+' -queueName KIE.RESPONSE.ALL ]')

AdminTask.createSIBDestination('[-bus '+rhbpmsBusName+' -name KIE.SESSION -type Queue -reliability ASSURED_PERSISTENT -description  -node '+node+' -server '+serverName+' ]')
AdminTask.createSIBJMSQueue(server, '[-name KIE.SESSION -jndiName jms/KIE.SESSION -busName '+rhbpmsBusName+' -queueName KIE.SESSION ]')
AdminTask.createSIBJMSActivationSpec(server, '[-name KIE.SESSION -jndiName jms/activation/KIE.SESSION -destinationJndiName jms/KIE.SESSION -busName '+rhbpmsBusName+' -destinationType javax.jms.Queue ]')

AdminTask.createSIBDestination('[-bus '+rhbpmsBusName+' -name KIE.TASK -type Queue -reliability ASSURED_PERSISTENT -description  -node '+node+' -server '+serverName+' ]')
AdminTask.createSIBJMSQueue(server, '[-name KIE.TASK -jndiName jms/KIE.TASK -busName '+rhbpmsBusName+' -queueName KIE.TASK ]')
AdminTask.createSIBJMSActivationSpec(server, '[-name KIE.TASK -jndiName jms/activation/KIE.TASK -destinationJndiName jms/KIE.TASK -busName '+rhbpmsBusName+' -destinationType javax.jms.Queue ]')

AdminTask.createSIBDestination('[-bus '+rhbpmsBusName+' -name KIE.SERVER.REQUEST -type Queue -reliability ASSURED_PERSISTENT -description  -node '+node+' -server '+serverName+' ]')
AdminTask.createSIBJMSQueue(server, '[-name KIE.SERVER.REQUEST -jndiName jms/KIE.SERVER.REQUEST -busName '+rhbpmsBusName+' -queueName KIE.SERVER.REQUEST ]')
AdminTask.createSIBJMSActivationSpec(server, '[-name KIE.SERVER.REQUEST -jndiName jms/activation/KIE.SERVER.REQUEST -destinationJndiName jms/KIE.SERVER.REQUEST -busName '+rhbpmsBusName+' -destinationType javax.jms.Queue ]')

AdminTask.createSIBDestination('[-bus '+rhbpmsBusName+' -name KIE.SERVER.RESPONSE -type Queue -reliability ASSURED_PERSISTENT -description  -node '+node+' -server '+serverName+' ]')
AdminTask.createSIBJMSQueue(server, '[-name KIE.SERVER.RESPONSE -jndiName jms/KIE.SERVER.RESPONSE -busName '+rhbpmsBusName+' -queueName KIE.SERVER.RESPONSE ]')
AdminTask.createSIBJMSActivationSpec(server, '[-name KIE.SERVER.RESPONSE -jndiName jms/activation/KIE.SERVER.RESPONSE -destinationJndiName jms/KIE.SERVER.RESPONSE -busName '+rhbpmsBusName+' -destinationType javax.jms.Queue ]')


#######################################
# Create Environment Variables

AdminConfig.create('VariableSubstitutionEntry', varmap, '[[symbolicName "jbpm.ut.jndi.lookup"] [description ""] [value "jta/usertransaction"]]')
AdminConfig.create('VariableSubstitutionEntry', varmap, '[[symbolicName "kie.services.jms.queues.response"] [description ""] [value "jms/KIE.RESPONSE.ALL"]]')
AdminConfig.create('VariableSubstitutionEntry', varmap, '[[symbolicName "kie.services.rest.deploy.async"] [description ""] [value "false"]]')
AdminConfig.create('VariableSubstitutionEntry', varmap, '[[symbolicName "kie.server.jms.queues.response"] [description ""] [value "jms/conn/KIE.SERVER.RESPONSE"]]')
AdminConfig.create('VariableSubstitutionEntry', varmap, '[[symbolicName "org.jboss.logging.provider"] [description ""] [value "jdk"]]')

AdminConfig.save();


