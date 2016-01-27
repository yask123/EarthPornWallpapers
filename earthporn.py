import praw
from PIL import Image
import requests
import shutil
import os
import time
import pwd
import argparse
import sys


def sanitize(link):
    if 'jpg' in link or 'png' in link:
        return link
    elif 'imgur' in link:
        return link + '.png'
    else:
        raise ValueError('cant sanitize url' + link)

def get_username():
    return pwd.getpwuid( os.getuid() )[ 0 ]

def main():
    description = "Set trending reddit images as wallpapers"
    parser = argparse.ArgumentParser(description = description)

    parser.add_argument("-sr", "--sub-reddit", default="EarthPorn",type=str, nargs='+',
        help="Sub reddit name, eg earthporn")
    parser.add_argument("-sort", "--sort-method", default="get_top_from_all", type=str, nargs='+',
        help="Sort method , eg: get_hot")
    parser.add_argument("-t", "--time", type=str, default="10", nargs='+',
        help="Time (in seconds) duration for each wallpaper")
    args = parser.parse_args()

    r = praw.Reddit(user_agent='RedditWallpaper Script by '+get_username())

    sub_reddit = args.sub_reddit
    sort_method = args.sort_method
    wall_duration = int(args.time)


    #submissions = r.get_subreddit(sub_reddit).get_top_from_all(limit=int(args.t))
    submissions = getattr(r.get_subreddit(str(sub_reddit)), str(sort_method))(limit= 10)


    my_dir = os.path.expanduser('~/.epwallpapers')

    #Create .epwallpapers directory to store all images
    if not os.path.exists(my_dir):
        os.makedirs(my_dir)

    i = 0
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
        with open(my_dir + '/' + str(i) + '.' + imgext, 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)

        imagePath = my_dir + '/' + str(i) + '.' + imgext

        with Image.open(imagePath) as im:
            width, height = im.size
            # We only want high resolution images
            if int(width) < 2000 or int(height) < 1300:
                continue

        osxcmd = 'osascript -e \'tell application "Finder" to set desktop picture to POSIX file "' + imagePath + '" \''
        os.system(osxcmd)
        print 'Done'

        i += 1
        if i == wcounts:
            i = 0
        time.sleep(wall_duration)


if __name__ == '__main__':
    main()
