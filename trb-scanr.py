import time
import sqlite3

sqlite_file = 'trb-scanr.sqlite'

# Press EXIT to close application
# Press RESULTS to show results
# Press CLEAN to clean DB
# Press CREATE to create a clean DB

if __name__ == "__main__":
	db = sqlite3.connect(sqlite_file)
	c = db.cursor()
	
	print("Connection to database established!")
	timeout = int(input("Timeout between scans should exceed (in seconds): "))
	print("OK! Let's get going!")
	
	while True:
		tagID = input("Input: ")
		if tagID == "EXIT":
			db.close()
			break
		elif tagID == "RESULTS":
			print("\n\n---RESULTS---\n")
			for row in c.execute('select tracks.tagID, runners.runnerID, runners.name, count(*) from tracks left join tags on tracks.tagID = tags.tagID left join runners on tags.runnerID = runners.runnerID group by tracks.tagID order by count(*) desc'):
				print("Runner {0} ({1}) was registered {2} times".format(row[2], row[0], row[3]))
			print("\n---END---\n\n")
		elif tagID == "CLEAN":
			c.execute('DELETE FROM tracks')
			print("DB cleaned!")
		elif tagID == "CREATE":
			c.execute("CREATE TABLE 'runners' ( 'runnerID' INTEGER NOT NULL, 'name' TEXT, PRIMARY KEY('runnerID') )")
			c.execute("CREATE TABLE 'tags' ( 'tagID' INTEGER NOT NULL UNIQUE, 'runnerID' INTEGER, PRIMARY KEY('tagID') )")
			c.execute("CREATE TABLE 'tracks' ( 'tagID' INTEGER NOT NULL, 'timestamp' INTEGER NOT NULL )")
			print("Tables created!")
		else:
			cTime = int(time.time())
			c.execute('SELECT * FROM tracks WHERE timestamp > ? AND tagID = ?', (cTime - timeout, tagID))
			if len(c.fetchall()) == 0:
				c.execute('''INSERT INTO tracks(tagID, timestamp) VALUES(?,?)''', (tagID, cTime))
				db.commit()
				c.execute('select * from tracks left join tags on tracks.tagID = tags.tagID left join runners on tags.runnerID = runners.runnerID WHERE tracks.tagID = ?', (tagID,))
				tResults = c.fetchall()
				print("Runner {0} ({1}) was registered {2} times".format(tResults[0][5], tagID, len(tResults)))
