
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
appName = "rhbpms-dashbuilder"

print "Installing dashbuilder application"
AdminApp.install(rhbpmsFileRoot+'/dashbuilder.war', '[ -appname '+appName+' -contextroot dashbuilder  -MapResRefToEJB [[ dashbuilder "" dashbuilder.war,WEB-INF/web.xml jdbc/dashbuilder javax.sql.DataSource jdbc/dashbuilder "" "" "" ]] -MapModulesToServers [[ .* .* '+server+' ]] -MapWebModToVH [[ .* .* default_host ]] -CtxRootForWebMod [[ .* .* dashbuilder ]]]' )


print "Mapping groups to users"
AdminApp.edit(appName, '[  -MapRolesToUsers ['
+'[ admin AppDeploymentOption.No AppDeploymentOption.No "" admin AppDeploymentOption.No "" group:defaultWIMFileBasedRealm/cn=admin,o=defaultWIMFileBasedRealm ]'
+'[ user AppDeploymentOption.No AppDeploymentOption.No "" user AppDeploymentOption.No "" group:defaultWIMFileBasedRealm/cn=user,o=defaultWIMFileBasedRealm ]]]')


print "Saving changes"
AdminConfig.save();


print "Starting dashbuilder"
appManager = AdminControl.queryNames('cell=*,node=*,type=ApplicationManager,process=server1,*')
AdminControl.invoke(appManager, 'startApplication', appName)

print "Saving changes"
AdminConfig.save();



