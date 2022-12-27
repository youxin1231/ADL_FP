import datetime
import praw
import pandas as pd
import json
from pathlib import Path

from praw.models import MoreComments

def get_date(submission):
	time = submission.created
	return datetime.datetime.fromtimestamp(time)

reddit = praw.Reddit(client_id='KlrsVYq2sbLo3x4VICco8w',
                     client_secret='4AGHhfwOH2MT5hnnw1EjfYGVO5ZPrg',
                     user_agent='wjiWIJji129nf')

hot_posts = reddit.subreddit('movies').new(limit=200)

posts = []

for i, post in enumerate(hot_posts):
    if i != 0 and i != 1: # filter the sticky article
        if len(post.selftext) >= 256:
            if not 'https' in post.selftext:
                submission = reddit.submission(id=post.id)
                dates = get_date(submission).strftime("%m/%d/%Y, %H:%M:%S")
                print(dates)
                posts.append([post.title,post.selftext, dates])

posts = pd.DataFrame(posts,columns=['title','body','date'])
result = posts.to_json(orient="records")
parsed = json.loads(result)

# data cleaning
for i in parsed:
    i['title'] = i['title'].replace('\n', ' ')
    i['body'] = i['body'].replace('\n', ' ')
    i['title'] = i['title'].replace('\r', ' ')
    i['body'] = i['body'].replace('\r', ' ')
    i['title'] = i['title'].replace('\u2019', '\'')
    i['body'] = i['body'].replace('\u2019', '\'')
    i['title'] = i['title'].replace('\u2018', '\'')
    i['body'] = i['body'].replace('\u2018', '\'')
    i['title'] = i['title'].replace('\"', '')
    i['body'] = i['body'].replace('\"', '')

json_object = json.dumps(parsed, indent=4, ensure_ascii=False)

outfile = Path('../data/movies1227.json')
outfile.write_text(json_object, encoding='UTF-8')