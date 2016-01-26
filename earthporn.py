import praw
from PIL import Image
import requests
import shutil
import os
import time
def sanitize(link):
	if 'jpg' in link or 'png' in link: 
		return link
	elif 'imgur' in link:
		return link+'.png'	
	else:
		raise ValueError ('cant sanitize url'+link)
		return None

def main():
	r = praw.Reddit(user_agent='Test Script by /u/yask')
	submissions = r.get_subreddit('EarthPorn').get_top_from_all(limit=10)
	my_dir = os.path.expanduser('~/.epwallpapers')
	
	if not os.path.exists(my_dir):
		os.makedirs(my_dir)
	i=0
	wlinks = []
	for each in submissions:
		wlinks.append(each)
	wcounts = len(wlinks)

	while True:	
		each = wlinks[i]
		try:
			url = sanitize(each.url)
			imgext = url.split('.')[-1]
		except ValueError as e:
			print e
			continue
		response = requests.get(url, stream=True)

		# Download images in  ~/.epwallpapers directory all images
		with open(my_dir+'/'+str(i)+'.'+imgext, 'wb') as out_file:
			shutil.copyfileobj(response.raw, out_file)

		imagePath = my_dir+'/'+str(i)+'.'+imgext
		osxcmd = 'osascript -e \'tell application "Finder" to set desktop picture to POSIX file "'+imagePath+'" \'' 	
		os.system (osxcmd)	
		print 'Done'
		i+=1
		if i == wcounts:
			i=0
		time.sleep(1)

if __name__ == '__main__':
	main()
