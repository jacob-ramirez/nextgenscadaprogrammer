# 8.0
# from com.inductiveautomation.ignition.gateway import IgnitionGateway
# 7.9
from com.inductiveautomation.ignition.gateway import SRContext
from com.inductiveautomation.ignition.common.model import ApplicationScope 

sessionManager = SRContext.get().getGatewaySessionManager()
# com.inductiveautomation.ignition.gateway.clientcomm
# Interface GatewaySessionManager

# java.util.List<ClientReqSession> findSessions(int scope)
sessions = sessionManager.findSessions(ApplicationScope.CLIENT)
for session in sessions:
	# com.inductiveautomation.ignition.gateway.clientcomm
	# Class ClientReqSession
	# Try to find all methods for session variable type
	clientID = session.getPublicId()
	if currentValue.value == clientID:
		# user terminating the client
		userName = ' ' # Put your admin username here

		# notification message sent to this session's client
		# addNotification(java.lang.String moduleId, java.lang.String messageType, java.io.Serializable message)
		# Adds a notification message that will be sent down to this session's client and delivered as a PushNotification.
		session.addNotification("", "remote-terminate", userName)

		# setMaxInactiveInterval(int interval)
		# Specifies the time, in seconds, between client requests before the servlet container will invalidate this session.
		session.setMaxInactiveInterval(0)
		system.tag.write(tagPath, "")
