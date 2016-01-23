import praw
from PIL import Image
import requests
import shutil

r = praw.Reddit(user_agent='Test Script by /u/yask')
submissions = r.get_subreddit('EarthPorn').get_top_from_all(limit=10)

import os
i=0
for each in submissions:
	#im = Image.open(each.url)
	url = each.url
	response = requests.get(url, stream=True)
	with open(str(i)+'.png', 'wb') as out_file:
		shutil.copyfileobj(response.raw, out_file)
	imagePath = os.getcwd()+'/'+str(i)+".png"	
	os.system ('osascript -e \'tell application "Finder" to set desktop picture to POSIX file "'+imagePath+'" \'')	
	print each.url
	i+=1
