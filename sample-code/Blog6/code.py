# This is to get the gateway version 
ver = system.net.httpGet('http://172.18.16.80:8088/main/system/gwinfo')
ver = ver.split(';')[3].split('=')[1][0]
if ver == "7":
from com.inductiveautomation.ignition.gateway import SRContext
	sessionManager = SRContext.get().getGatewaySessionManager()
else:
	# Line below is for Ignition 8
	from com.inductiveautomation.ignition.gateway import IgnitionGateway
	sessionManager = IgnitionGateway.get().getGatewaySessionManager()

# java.util.List<ClientReqSession> findSessions(int scope)
from com.inductiveautomation.ignition.common.model import ApplicationScope
sessions = sessionManager.findSessions(ApplicationScope.CLIENT)

# Get Database connection strings
dbRead = system.tag.read("Databases/Read/Log_X").value
dbWrite = system.tag.read("Databases/Write/Log_X").value
sql = "INSERT INTO SCADA_LOG_X.UserSessions (UTCTimeStamp, CSTTimeStamp, CSTCreationDate, Username, ClientId, Hostname, IPAddress) VALUES (?, ?, ?, ?, ?, ?, ?)"
# Loop through all the vision client sessions
for session in sessions:
	clientID = session.getPublicId()
	# Now call the built in session info function to get [username, address (hostname), clientId, creationTime]
	for row in system.util.getSessionInfo():
		if row["clientId"] == clientID:
			timeStampCST = system.date.now()
			timeStampUTC = system.date.addHours(timeStampCST, abs(int(system.date.getTimezoneOffset())))
			creationDateCST = row["creationTime"]
			username = row["username"]
			hostname = row["address"]

			# Function from ApplicationScope class
			ip = session.getAttribute('remoteAddr')

			# Now check if that client ID is not already in the database
			rowCountInDB = int(str(system.db.runScalarPrepQuery("SELECT COUNT(*) FROM SCADA_LOG_X.UserSessions WHERE ClientId = ? AND Username = ?", [clientID, username], dbRead)))
			if rowCountInDB == 0:
				# It's not in the db already, so now insert a new row
				system.db.runPrepUpdate(sql, [timeStampUTC, timeStampCST, creationDateCST, username, clientID, hostname, ip], dbWrite)