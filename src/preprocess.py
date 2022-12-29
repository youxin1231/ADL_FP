import json
from pathlib import Path 

def main():
    # Opening JSON file
    f = open('./data/labeled.json')

    # returns JSON object as 
    # a dictionary
    data = json.load(f)
    
    load_data = []

    for post in data:
        title = post['title'][:-1]
        label = post['label']
        if label is not None:
            load_data.append(f'{title}####{label}')

    train_data = load_data[:int(0.8*len(load_data))]
    eval_data = load_data[int(0.8*len(load_data))+1:]
    
    f = open('./processed_data/train.txt', 'w')
    for i in train_data:
        if i == train_data[len(train_data)-1]:
            f.write(f'{i}')
        else:
            f.write(f'{i}\n')

    f.close()

    f = open('./processed_data/eval.txt', 'w')
    for i in eval_data:
        if i == eval_data[len(eval_data)-1]:
            f.write(f'{i}')
        else:
            f.write(f'{i}\n')

    f.close()

if __name__ == '__main__':
    main()