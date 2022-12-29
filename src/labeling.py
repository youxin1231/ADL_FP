import json
from pathlib import Path
import pandas as pd

# Opening JSON file
f = open('../data/roger.json')

# returns JSON object as 
# a dictionary
data = json.load(f)


i = 0
while(i != len(data)):
    post = data[i]
    post['label'] = '['
    while(1):
        print('------------------------------------')
        print(f'[{i}] # Input \'q\' to quit sentence, \'u\' undo last action.')
        print(post['title'])
        print(post['index'])

        # input q for quit, u for undo
        aspect = input('Aspect: ')
        if 'q' in aspect:
            break
        elif 'u' in aspect:
            post['label'] = '['
            continue
        opinion = input('Opinion: ')
        if 'q' in opinion:
            break
        elif 'u' in opinion:
            post['label'] = '['
            continue        
        sentiment = input('Sentiment(p,n,N): ')
        if 'q' in sentiment:
            break
        elif 'u' in sentiment:
            post['label'] = '['
            continue  
        
        aspect = list(map(int,aspect.split()))
        opinion = list(map(int,opinion.split()))

        if sentiment == 'p':
            sentiment = 'POS'
        elif sentiment == 'n':
            sentiment = 'NEG'
        else:
            sentiment = 'NEU'

        aspect = [i for i in range(aspect[0], aspect[-1]+1)]
        opinion = [i for i in range(opinion[0], opinion[-1]+1)]
        post['label'] += f'({aspect},{opinion},\'{sentiment}\'),'

    i += 1

    post['label'] = post['label'][:-1]
    post['label'] += ']'
    if post['label'] == ']':
        post['label'] = None
    posts = pd.DataFrame(data,columns=['title','index','label','body'])
    result = posts.to_json(orient="records")
    parsed = json.loads(result)

    json_object = json.dumps(parsed, indent=4, ensure_ascii=False)

    outfile = Path('./labeled.json')
    outfile.write_text(json_object, encoding='UTF-8')