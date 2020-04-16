#coding=UTF-8
import lxml
import requests
import time
import sys
import progress_bar as PB
import json

YOUTUBE_IN_LINK = 'https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&maxResults=100&order=relevance&pageToken={pageToken}&videoId={videoId}&key={key}'
YOUTUBE_LINK = 'https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&maxResults=100&order=relevance&videoId={videoId}&key={key}'
key = 'AIzaSyA6vj3BjmIw0CrybmiL6YkwEZzaybK0MC4'  #改为申请的google api
	

def commentExtract(videoId, count = -1):
	print ("\nComments downloading")
	#关闭http连接，增加重连次数



	page_info = requests.get(YOUTUBE_LINK.format(videoId = videoId, key = key))
	while page_info.status_code != 200:
		if page_info.status_code != 429:
			print ("Comments disabled")
			sys.exit()

		time.sleep(20)
		page_info = requests.get(YOUTUBE_LINK.format(videoId = videoId, key = key))

	page_info = page_info.json()
	#test
	# print(page_info)

	comments = []
	co = 0;
	for i in range(len(page_info['items'])):
		if page_info['items'][i]['snippet']['topLevelComment']['snippet']['likeCount']>=3000:
			comments.append(page_info['items'][i]['snippet']['topLevelComment']['snippet']['textOriginal'])
			co += 1
		if co == count:
			PB.progress(co, count, cond = True)
			return comments

	PB.progress(co, count)
	# INFINTE SCROLLING
	while 'nextPageToken' in page_info:
		temp = page_info
		page_info = requests.get(YOUTUBE_IN_LINK.format(videoId = videoId, key = key, pageToken = page_info['nextPageToken']))

		while page_info.status_code != 200:
			time.sleep(20)
			page_info = requests.get(YOUTUBE_IN_LINK.format(videoId = videoId, key = key, pageToken = temp['nextPageToken']))
		page_info = page_info.json()

		for i in range(len(page_info['items'])):
			comments.append(page_info['items'][i]['snippet']['topLevelComment']['snippet']['textOriginal'])
			co += 1
			if co == count:
				PB.progress(co, count, cond = True)
				return comments
		PB.progress(co, count)
	PB.progress(count, count, cond = True)
	print ()

	return comments
