# WebSphere App Server configuration script for 
# /opt/IBM/WebSphere8.5.5_Dev/AppServer/profiles/AppSrv01/bin/wsadmin.sh -lang jython -f /opt/rh/bpms/config-was-for-bpm.py

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


#######################################
## Install a WAR file
appName = "rhbpms-business-central"


print "Installing business-central application"
AdminApp.install(rhbpmsFileRoot+'/business-central.war', '[ -appname '+appName+' '
+'-contextroot business-central '
+'-MapWebModToVH [[.* .* default_host ]] '
+'-CtxRootForWebMod [[.* .* business-central ]] '
+'-MapResRefToEJB ['
	+'[ business-central.war KieSessionRequesMessageBean business-central.war,WEB-INF/ejb-jar.xml org.kie.remote.services.jms.RequestMessageBean/factory javax.jms.ConnectionFactory jms/conn/KIE.RESPONSE.ALL "" "" "" ]'
	+'[ business-central.war TaskServiceRequesMessageBean business-central.war,WEB-INF/ejb-jar.xml org.kie.remote.services.jms.RequestMessageBean/factory javax.jms.ConnectionFactory jms/conn/KIE.RESPONSE.ALL "" "" "" ]] '
+'-BindJndiForEJBMessageBinding ['
	+'[ business-central.war KieSessionRequesMessageBean business-central.war,WEB-INF/ejb-jar.xml "" jms/activation/KIE.SESSION "" "" ]'
	+'[ business-central.war TaskServiceRequesMessageBean business-central.war,WEB-INF/ejb-jar.xml "" jms/activation/KIE.TASK "" "" ]'
	+'[ business-central.war JMSAuditProcessor business-central.war,WEB-INF/ejb-jar.xml "" jms/activation/KIE.AUDIT "" "" ]]'
+']' )

print "Mapping groups to users"
AdminApp.edit(appName, '[  -MapRolesToUsers ['
+'[ admin AppDeploymentOption.No AppDeploymentOption.No "" admin AppDeploymentOption.No "" group:defaultWIMFileBasedRealm/cn=admin,o=defaultWIMFileBasedRealm ]'
+'[ developer AppDeploymentOption.No AppDeploymentOption.No "" developer AppDeploymentOption.No "" group:defaultWIMFileBasedRealm/cn=developer,o=defaultWIMFileBasedRealm ]'
+'[ analyst AppDeploymentOption.No AppDeploymentOption.No "" analyst AppDeploymentOption.No "" group:defaultWIMFileBasedRealm/cn=analyst,o=defaultWIMFileBasedRealm ]'
+'[ manager AppDeploymentOption.No AppDeploymentOption.No "" manager AppDeploymentOption.No "" group:defaultWIMFileBasedRealm/cn=manager,o=defaultWIMFileBasedRealm ]'
+'[ user AppDeploymentOption.No AppDeploymentOption.No "" user AppDeploymentOption.No "" group:defaultWIMFileBasedRealm/cn=user,o=defaultWIMFileBasedRealm ]]]')


print "Setting classloader to single"
bcaId = AdminConfig.getid('/Deployment:'+appName+'/')
bcaDepObject = AdminConfig.showAttribute(bcaId, 'deployedObject')
AdminConfig.show(bcaDepObject, 'warClassLoaderPolicy')
AdminConfig.modify(bcaDepObject, [[ 'warClassLoaderPolicy', 'SINGLE' ]])

print "Setting classloader mode to parent-last"
bcaClassloader = AdminConfig.showAttribute(bcaDepObject, 'classloader')
AdminConfig.show(bcaClassloader, 'mode')
AdminConfig.modify(bcaClassloader, [['mode', 'PARENT_LAST']])

print "Adding bouncy castle variables"
#   http://www-01.ibm.com/support/knowledgecenter/SSAW57_7.0.0/com.ibm.websphere.nd.doc/info/ae/ae/txml_applibrary.html
AdminConfig.create('VariableSubstitutionEntry', varmap, '[[symbolicName "org.apache.sshd.registerBouncyCastle"] [description ""] [value "true"]]')
AdminConfig.create('VariableSubstitutionEntry', varmap, '[[symbolicName "org.uberfire.domain"] [description ""] [value "WSLogin"]]')

print "Adding bouncy castle shared library reference"
AdminConfig.create('Library', server, '[[nativePath ""] [name "bouncyCastle"] [isolatedClassLoader "false"] [description ""] [classPath "bcprov-jdk16-1.46.jar"]]')
AdminConfig.create('LibraryRef', bcaClassloader, [['libraryName', 'bouncyCastle']])

print "Saving changes"
AdminConfig.save();

print "Starting business-central"
#appManager = AdminControl.queryNames('cell=*,node=*,type=ApplicationManager,process=server1,*')
#AdminControl.invoke(appManager, 'startApplication', appName)

print "Saving changes"
AdminConfig.save();



