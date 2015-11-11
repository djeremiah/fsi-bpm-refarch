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
appName = "rhbpms-kieserver"

print "Installing kie-server application"
AdminApp.install(rhbpmsFileRoot+'/kie-server.war', '[ -appname '+appName+' -contextroot kie-server  '
+'-MapResRefToEJB [[ KieServer KieServerMDB kie-server.war,WEB-INF/ejb-jar.xml org.kie.server.jms.KieServerMDB/factory javax.jms.ConnectionFactory jms/conn/KIE.SERVER.REQUEST "" "" "" ]] '
+'-MapModulesToServers [[ KieServer kie-server.war,WEB-INF/web.xml '+server+' ]] '
+'-MapWebModToVH [[ .* .* default_host ]] '
+'-CtxRootForWebMod [[ .* .* kie-server ]] '
+'-BindJndiForEJBMessageBinding [[ KieServer KieExecutorMDB kie-server.war,WEB-INF/ejb-jar.xml "" jms/activation/KIE.EXECUTOR "" "" ][ KieServer KieServerMDB kie-server.war,WEB-INF/ejb-jar.xml "" jms/activation/KIE.SERVER.REQUEST "" "" ]]'
+']' )


print "Mapping groups to users"
AdminApp.edit(appName, '[  -MapRolesToUsers ['
+'[ kie-server AppDeploymentOption.No AppDeploymentOption.No "" kie-server AppDeploymentOption.No "" group:defaultWIMFileBasedRealm/cn=kie-server,o=defaultWIMFileBasedRealm ]]]')


print "Setting classloader to single"
appId = AdminConfig.getid('/Deployment:'+appName+'/')
depObject = AdminConfig.showAttribute(appId, 'deployedObject')
AdminConfig.show(depObject, 'warClassLoaderPolicy')
AdminConfig.modify(depObject, [[ 'warClassLoaderPolicy', 'SINGLE' ]])

print "Setting classloader mode to parent-last"
appClassloader = AdminConfig.showAttribute(depObject, 'classloader')
AdminConfig.show(appClassloader, 'mode')
AdminConfig.modify(appClassloader, [['mode', 'PARENT_LAST']])

print "Saving changes"
AdminConfig.save();

print "Starting kie-server"
appManager = AdminControl.queryNames('cell=*,node=*,type=ApplicationManager,process=server1,*')
AdminControl.invoke(appManager, 'startApplication', appName)

print "Saving changes"
AdminConfig.save();



