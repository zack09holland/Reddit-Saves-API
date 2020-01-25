############################################
# Reddit saves program by Zachary Holland
#	This program was created to organize my saves on Reddit to allow me 
#	to quickly find a post that I am interested in knowing. The program
#	will go through the list of any user' saves and grab the necessary 
#	information using PRAW. After the information is stored, a holding
#	directory is created to store each subreddit directory and its 
#	corresponding postings
#
############################################
# Usage
# 1. Create a text file containing Reddit username and password split by a space
# 2. python redditSaves.py name_of_login_info.txt
# 3. View results of your saved posts on Reddit in the directory 'SubReddits'
############################################
import praw
import sys
import pprint 
import os
import shutil
"""
	Create the user_agent and parser for using the RedditAPI
"""
user_agent = "Organize saves 1.0 by /u/zack09holland"
r = praw.Reddit(user_agent = user_agent)

"""
	Get the username and password from the classified file
	passed in as an argument. 
"""
filename = str(sys.argv[1])
fileinfo = open(filename,'r')
loginInfo = fileinfo.readline().split(' ')
fileinfo.close()
username = loginInfo[0]
password = loginInfo[1]

r.login(username,password,disable_warning = True)

"""
	Create the main directory and then create folders within it for 
	each SubReddit to hold the information of the different saves

"""
if os.path.exists("SubReddits"):
	shutil.rmtree("SubReddits")	# Remove it so a new one can be made
	# Only way to create a directory without an error
	# was to check if the path did not exist
	if not os.path.exists("SubReddits"):
		os.mkdir("SubReddits")
else:
	os.mkdir("SubReddits")

	
# Take in the subredditname(path) and the package(input) to be displayed
def createSubDirectory (path,input):
	here = os.path.dirname(os.path.realpath(__file__))
	folder = 'SubReddits'+'\\'+ path
	filename = path + "Saves.txt"
	subFilePath = os.path.join(here,folder,filename)
	# If the path joined together doesn't exist create it and write to it
	# otherwise just append to the file
	if not os.path.exists(os.path.join(here,folder)):
		os.mkdir(os.path.join(here,folder))
		f = open(subFilePath,'w')
		f.write(input+'\n')
	else:
		f = open(subFilePath,'a')
		f.write(input+'\n')	
		
"""
	Go through the saves for the user and write all of them to  
	the SavedList file, keeping track of the count for the total
	as well as for individual subreddit's 
"""
subDictionary = {}		# Dictionary to hold the subreddits and their count
totalcount = 0
fileSave = open("SavedList",'w')	


for posts in r.user.get_saved(limit = 25):
	totalcount += 1
	try:
		post = str(posts).split(' :: ')	
		postname = post[1]
		subRedditName = str(posts.subreddit.display_name)
		link = posts.short_link
		package = '['+subRedditName+'] '+postname+'\n'+link
		createSubDirectory(subRedditName,package)		
		# If the dictionary contains the key update the count for the key
		# Otherwise create an entry for the subreddit
		if subDictionary.has_key(subRedditName):
			subDictionary[subRedditName] += 1
		else:
			subDictionary.setdefault(subRedditName,1)
		
	except Exception:
		pass
	# Create the printable package to be displayed
	#package = '['+subRedditName+'] '+postname+'\n'+link
	
	fileSave.write(package+'\n')		# Send to an output file
# After looping through all  user saves close the fileSave file	
fileSave.close()
"""
	Output the final results of the analysis
"""	
print '+-------------------------------+'
print 'Total count: %s \n' % (totalcount)
pprint.pprint(subDictionary)
#sort function of a map or dictionary
