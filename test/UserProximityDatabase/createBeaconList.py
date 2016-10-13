import MySQLdb

def check():
	dl = MySQLdb.connect("localhost", "root", "seelab")
	cur = dl.cursor()
	sql = "SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = 'BeaconDatabase'"
	
	try:
		cur.execute(sql)
		results = cur.fetchall()
		dl.close()
		if len(results) == 0:
			return(0)
		else:
			return(1)
	except:
		dl.close()
		print("check: mysql connection error")

def createDatabase():
	dz = MySQLdb.connect("localhost", "root", "seelab")
	cu = dz.cursor()
	sq = "CREATE DATABASE IF NOT EXISTS BeaconDatabase"

	try:
		cu.execute(sq)
		print("BeaconDatabase created")
		s = "USE BeaconDatabase"
		cu.execute(s)
		sql = "CREATE TABLE UserData(UID INT, PID BIGINT, NAME VARCHAR(20))"
		cu.execute(sql)
		print("UserData table created")
		sql = "CREATE TABLE BeaconData(UID INT, UUID VARCHAR(20), MAJOR INT, MINOR INT, TXPOWER INT, LOCATION VARCHAR(20))"
		cu.execute(sql)
		print("BeaconData table created")
		sql = "CREATE TABLE ProximityData(UID INT, PID BIGINT, BEACON INT, YEAR INT, MONTH INT, DAY INT, HOUR INT, MINUTE INT, SECOND INT, TIME DATETIME, DIST FLOAT, RSSI INT, STATUS TINYINT)"
		cu.execute(sql)
		print("ProximityData table created")
		sql = "CREATE USER 'beaconuser'@'%' IDENTIFIED BY 'seelab'"
		cu.execute(sql)
		print("User for phone app to access database created")
		sql = "GRANT ALL PRIVILEGES ON *.* TO 'beaconuser'@'%'"
		cu.execute(sql)
		sql = "FLUSH PRIVILEGES"
		cu.execute(sql)
		print("Privileges set")
		dz.close()
		return(1)
	except:
		print("create: mysql connection error")
		dz.close()
		return(0)

def deleteDatabase():
	dz = MySQLdb.connect("localhost", "root", "seelab")
	cu = dz.cursor()
	sq = "DROP DATABASE BeaconDatabase"

	try:
		cu.execute(sq)
		print("Existing BeaconDatabase deleted")
		sql = "DROP USER 'beaconuser'@'%'"
		cu.execute(sql)
		print("User removed")
		dz.close()
		return(1)
	except:
		print("delete: error deleting existing database")
		dz.close()
		return(0)
	

def create():
	print("Beginning to create the Beacon database...")
	if check() == 1:
		print("The database already exist")
		ans1 = raw_input("Would you like to delete existing data and create a new one? (y/n)")
		if ans1 == 'y':
			ans2 = raw_input("Are you sure? (y/n)")
			if ans2 == 'y':
				deleteDatabase()
				create()
		return(0)
	
	if createDatabase() == 1:
		print("Database successfully created")
		return(1)
	else:
		print("Error when creating database, exiting")
		return(0)

def delete():
	ans = raw_input("Are you sure? (y/n)")
	if ans != 'y':
		return(0)
	print("Beginnning to delete the Beacon database...")
	if check() != 1:
		print("The database doesn't exist")
		return(0)
	if deleteDatabase() == 1:
		print("Database successfully deleted")
		return(1)

def add():
	if check() != 1:
		print("The database doesn't exist")
		return(0)
	
	dl = MySQLdb.connect("localhost", "root", "seelab", "BeaconDatabase")
	cur = dl.cursor()
	uid = raw_input("Enter your UID (House ID): ")
	uuid = raw_input("Enter the UUID of the beacon (including dashes): ")
	major = raw_input("Enter the major number of the beacon: ")
	next = 'y'
	while next == 'y':
		minor = raw_input("Enter the minor number of the beacon: ")
		txpower = raw_input("Enter the txpower of the beacon: ")
		location = raw_input("Enter the location of the beacon (ex. fridge, microwave):")

		sq = "INSERT INTO BeaconData VALUES" + str((uid, uuid, major, minor, txpower, location))
		print sq
		try:
			cur.execute(sq)
			dl.commit()
			print("Beacon successfully added to the table")
		except:
			print("add: error in inserting new beacon")
			break

		next = raw_input("Do you have another beacon that you want to add? Make sure they have the same UUID and major number as the previous one. (y/n)")
	dl.close()

def remove():
	if check() != 1:
		print("The database doesn't exist")
		return(0)
	
	dl = MySQLdb.connect("localhost", "root", "seelab", "BeaconDatabase")
	cur = dl.cursor()
	minor = raw_input("Enter the minor number of the beacon that you want to remove: ")
	sq = "DELETE FROM BeaconData WHERE MINOR = " +str(minor);
	print sq
	try:
		cur.execute(sq)
		dl.commit()
		print("Beacon successfully removed")
	except:
		print("remove: error in removing beacon")
	dl.close()

def order():
	if check() != 1:
		print("The database doesn't exist")
		return(0)

	dl = MySQLdb.connect("localhost","root","seelab","BeaconDatabase")
	cur = dl.cursor()
	sq = "SELECT * FROM BeaconData"
	print("UUID, Major, Minor, TXPower, Location")
	try:
		cur.execute(sq)
		for row in cur:
			print row
	except:
		print("order client format error")
	dl.close()
	return(1)

def main():
	while(True):
		print("")
		print("Welcome to Beacon Setup of Home Automation")
		print("Choose one of the below options")
		print("1 - Create beacon database")
		print("2 - Add beacon")
		print("3 - Remove beacon")
		print("4 - List beacons")
		print("5 - Delete beacon database")
		print("6 - Exit")
		choice = raw_input("Enter from 1-6: ")
		if choice == '1':
			create()
		elif choice == '2':
			add()
		elif choice == '3':
			remove()
		elif choice == '4':
			order()
		elif choice == '5':
			delete()
		elif choice == '6':
			break
		else:
			print("Invalid choice")

if __name__ == '__main__':
	main()
		
