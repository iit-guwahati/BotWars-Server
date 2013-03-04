from storm.locals import *
import time
from dbVars import *
import logging

class Team(object):
  __storm_table__ = "teams"
  teamId = Int(primary=True)
  teamName = Unicode()
  teamPassword = Unicode()
  teamEmail = Unicode()

class TeamScore(object):
  __storm_table__ = "teamscores" 
  entryId = Int(primary=True)
  teamId = Int()
  problemNo = Unicode()
  score = Int()

class Submission(object):
  __storm_table__ = "submissions"
  submissionId = Int(primary=True)
  teamId = Int()
  problemNo = Unicode()
  submissionTime = Int()
  filename = Unicode()
  score = Int()
  errors = Unicode()

db = create_database("mysql://" + db_user + ":" + db_pass + "@" + db_server + 
                     "/" + db_name)
store = Store(db)
store.execute("CREATE TABLE IF NOT EXISTS `submissions` (\
  `submissionId` int(11) NOT NULL AUTO_INCREMENT,\
  `teamId` int(11) NOT NULL,\
  `problemNo` varchar(5) NOT NULL,\
  `submissionTime` int(11) NOT NULL,\
  `filename` varchar(30) NOT NULL,\
  `score` int(11) NOT NULL,\
  `errors` varchar(100) NOT NULL,\
  PRIMARY KEY (`submissionId`)\
)")
store.execute("CREATE TABLE IF NOT EXISTS `teams` (\
  `teamId` int(11) NOT NULL AUTO_INCREMENT,\
  `teamName` varchar(20) NOT NULL,\
  `teamPassword` varchar(20) NOT NULL,\
  `teamEmail` varchar(20) NOT NULL,\
  PRIMARY KEY (`teamId`)\
)")
store.execute("CREATE TABLE IF NOT EXISTS `teamscores` (\
  `entryId` int(11) NOT NULL AUTO_INCREMENT,\
  `teamId` int(11) NOT NULL,\
  `problemNo` varchar(20) NOT NULL,\
  `score` int(11) NOT NULL,\
  PRIMARY KEY (`entryId`)\
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
    team = team.one()
  else:
    #Should never reach here
    return -1

  logging.debug("Before submission; team.teamId : %d", team.teamId)

  #add submission
  sub = Submission()
  sub.teamId = team.teamId
  sub.problemNo = unicode(problemNo)
  sub.submissionTime = submissionTime
  sub.filename = unicode(filename)
  sub.score = score
  sub.errors = unicode(errors)
  store.add(sub)
  
  logging.debug("After submission; team.teamId : %d", team.teamId)
  #check for maximum score for this question
  maxScore = store.find(TeamScore, TeamScore.teamId==team.teamId, TeamScore.problemNo==problemNo)
  for i in maxScore:
    logging.debug("Maxscore - id:  %d", i.teamId)

  if maxScore.count()>0:
    if maxScore.one().score<score:
      maxScore.set(score=score)
  else:
    newScore = TeamScore()
    newScore.teamId=team.teamId
    logging.debug("updating : %d, %d", team.teamId, newScore.teamId)
    newScore.problemNo=problemNo
    newScore.score=score
    store.add(newScore)
  store.flush()
  store.commit()
  return True

def getScores(teamname):
  global store
  team = store.find(Team, Team.teamName == unicode(teamname))
  if team.count()>0:
    teamId = team.one().teamId
  retStr = "Scores:\n------\n"
  submissions = store.find(Submission, Submission.teamId == teamId)
  for i in submissions:
    retStr=retStr+"Problem "+i.problemNo+" @ "+time.ctime(i.submissionTime)+"\n\tScore: "+str(i.score)+"\n\tErrors: "+i.errors+"\n"
  return retStr

def getLeaderboard():
  global store
  scores=store.find((TeamScore.teamId,TeamScore.problemNo,TeamScore.score)).group_by(TeamScore.teamId,TeamScore.problemNo)
  teamScores={}
  totalScores={}
  for (i,j,k) in scores:
    if i in teamScores:
      teamScores[i][j]=k
      totalScores[i]+=k
    else:
      teamScores[i]={j:k}
      totalScores[i]=k
  totalScores = sorted(totalScores.items(), key=lambda x: x[1])
  totalScores.reverse()
  retStr = "Leaderboard\n----------\n"
  for (i,j) in totalScores:
    retStr+=store.find(Team.teamName, Team.teamId==i).one()+": "+str(j)+"\n"
    for k in teamScores[i]:
      retStr+="\t"+k+": "+str(teamScores[i][k])+"\n"
  return retStr
