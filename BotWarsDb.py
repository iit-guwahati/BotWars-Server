from storm.locals import *

class Team(object):
	__storm_table__ = "teams"
	teamId = Int(primary=True)
	teamName = Unicode()
	teamPassword = Unicode()
	teamEmail = Unicode()

class Submission(object):
	__storm_table__ = "submissions"
	submissionId = Int(primary=True)
	teamId = Int()
	problemNo = Unicode()
	submissionTime = Int()
	filename = Unicode()
	score = Int()

db = create_database("mysql://BotWarsAdmin:BotWarsPassword@localhost/BotWarsDb")
store = Store(db)
store.exec("CREATE TABLE IF NOT EXISTS `submissions` (
  `submissionId` int(11) NOT NULL AUTO_INCREMENT,
  `teamId` int(11) NOT NULL,
  `problemNo` varchar(5) NOT NULL,
  `submissionTime` int(11) NOT NULL,
  `filename` varchar(30) NOT NULL,
  `score` int(11) NOT NULL,
  `errors` varchar(100) NOT NULL,
  PRIMARY KEY (`submissionId`)
)")
store.exec("CREATE TABLE IF NOT EXISTS `teams` (
  `teamId` int(11) NOT NULL AUTO_INCREMENT,
  `teamName` varchar(20) NOT NULL,
  `teamPassword` varchar(20) NOT NULL,
  `teamEmail` varchar(20) NOT NULL,
  PRIMARY KEY (`teamId`)
)")

def authenticate(teamname, teampassword):
	global store
	result = store.find(Team, Team.teamName == unicode(teamname))
	if result.count()>0:
		return result.one().teamPassword == teampassword
	return False

def updateSubmissions(teamname, problemNo, submissionTime, filename, score, errors):
	global store
	team = store.find(Team, Team.teamName == unicode(teamname))
	if team.count()>0:
		teamId = team.one().teamId
	sub = Submission()
	sub.teamId = teamId
	sub.problemNo = unicode(problemNo)
	sub.submissionTime = submissionTime
	sub.filename = unicode(filename)
	sub.score = score
	sub.errors = unicode(errors)
	store.add(sub)
	store.flush()
	store.commit()

#def getLeaderboard():
#	global store
#	store.find(
