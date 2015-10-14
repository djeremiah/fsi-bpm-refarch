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
adminUser = "admin"
adminPass = "Redhat1!"


#######################################
# Enable Admin and Appliation Security

AdminTask.applyWizardSettings('[-secureApps true -secureLocalResources false -adminPassword '+adminPass+' -userRegistryType WIMUserRegistry -adminName '+adminUser+' ]')

AdminConfig.save();


#######################################
# Set generic JVM arguments
AdminTask.setJVMProperties('[-nodeName '+node+' -serverName '+serverName+' -initialHeapSize 1024 -maximumHeapSize 4096 ]')


AdminConfig.save();


### **** Server must be restarted after changing heap and authentication settings **** 




