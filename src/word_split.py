import json
from pathlib import Path
import pandas as pd

# Opening JSON file
f = open('data/2774.json')

# returns JSON object as 
# a dictionary
data = json.load(f)


## data cleaning
for i, post in enumerate(data):
    for symbol in ['[',']','!','?','(',')','...','"','“','”','…','_','..','-']:
        post['title'] = post['title'].replace(symbol, '')

# Iterating through the json
# list

title = []
index = []
body = []

for i, post in enumerate(data):
    out1 = '' ; out2 = ''
    sum = 0

    body.append(post['body'])
    for j, word in enumerate(post['title'].split()):
        out1 += word + ' '
        if len(str(j)) > len(word):
            out1 += ' ' * (len(str(j)) - len(word))
        out2 += (f'{j:<{len(word)}}') + ' '

    print(f'{out1}\n{out2}')
    title.append(out1)
    index.append(out2)

result = []
for i, post in enumerate(data):
    result.append([title[i],index[i],body[i]])

posts = pd.DataFrame(result,columns=['title','index','body'])
result = posts.to_json(orient="records")
parsed = json.loads(result)

json_object = json.dumps(parsed, indent=4, ensure_ascii=False)

outfile = Path('data/raw_dataset.json')
outfile.write_text(json_object, encoding='UTF-8')

# Closing file
f.close()
