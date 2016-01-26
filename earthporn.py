import praw
from PIL import Image
import requests
import shutil
import os

def sanitize(link):
	if 'jpg' in link or 'png' in link: 
		return link
	elif 'imgur' in link:
		return each.url+'.png'	
	else:
		raise ValueError ('cant sanitize url'+link)
		return None

def main():
	r = praw.Reddit(user_agent='Test Script by /u/yask')
	submissions = r.get_subreddit('EarthPorn').get_top_from_all(limit=10)


	for i,each in enumerate(submissions):
		
		try:
			url = sanitize(each.url)
		except ValueError as e:
			print e
			continue
		response = requests.get(url, stream=True)

		# Download images in  ~/.epwallpapers directory all images
		os.mkdir('~/.epwallpapers')
		with open('~/.epwallpapers/'+str(i)+'.png', 'wb') as out_file:
			shutil.copyfileobj(response.raw, out_file)

		imagePath = '~/.epwallpapers/'+str(i)+'.png'
		osxcmd = 'osascript -e \'tell application "Finder" to set desktop picture to POSIX file "'+imagePath+'" \'' 	
		os.system (osxcmd)	
		print each.url

if __name__ == '__main__':
	main()
