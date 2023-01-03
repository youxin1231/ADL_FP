import praw
from psaw import PushshiftAPI
import json
import datetime as dt
start_time = dt.datetime.now()

def main():
    sub = input('Subreddit: ')

    dataset_size = 10000

    print('Connecting to pushshift server...')

    reddit = praw.Reddit(client_id='yZn7KcD7GMoerEt8tuoF_g',
                        client_secret='JuTvsef5FhiKOGmVgUAmGXIHZxhimQ',
                        user_agent='ADL_project')
    api = PushshiftAPI(reddit)
    # api = PushshiftAPI()

    print('Finish !')

    # start_epoch=int(dt.datetime(2022, 1, 1).timestamp())
    # end_epoch = int(dt.datetime(2022, 12, 25).timestamp())

    post_list = []

    print('Crawling...')
    submissions = api.search_submissions(
                                        # after=start_epoch,
                                        # before=end_epoch,
                                         size=500,
                                         subreddit=sub,
                                         fields='title,selftext')

    craw_cnt = 0; result_cnt = 0
    for post in submissions:
        craw_cnt += 1

        title = post.title
        body = post.selftext
        print(f'{craw_cnt}: {title}\n{body}')

        # If post body length >= 64, Add the post to dataset.

        if len(title) >= 20 and len(body) >= 64:
            # Preprocessing title, body.

            if not 'http' in body:
                title = title.replace('\n', ' ')
                body = body.replace('\n', ' ')
                title = title.replace('\r', ' ')
                body = body.replace('\r', ' ')
                title = title.replace('\u2019', '\'')
                body = body.replace('\u2019', '\'')
                title = title.replace('\u2018', '\'')
                body = body.replace('\u2018', '\'')
                title = title.replace('\"', '')
                body = body.replace('\"', '')

                post_list.append({'title':title, 'body':body})
                with open(f'{sub}.json', 'w', encoding='utf-8') as f:
                    json.dump(post_list, f, ensure_ascii=False, indent=2)

                result_cnt += 1
                print(f'----------Current_dataset_num: {result_cnt}/{dataset_size}----------')
                
                if result_cnt == dataset_size:
                    return
    
if __name__ == '__main__':
    main()
    print('Duration: {}'.format(dt.datetime.now() - start_time))