import json
from pathlib import Path 
import ast
from random import sample

def main():
    # Opening JSON file
    f = open('./data/labeled.json')

    # returns JSON object as 
    # a dictionary
    data = json.load(f)
    
    load_data = []

    for post in data:
        title = post['title'][:-1]
        label_text = post['label']
        if label_text is not None:
            labels = ast.literal_eval(label_text)
            POS = []; NEG = []; NEU = []
            for label in labels:
                if label[2] == 'POS':
                    POS.append(tuple(label[0]))
                elif label[2] == 'NEG':
                    NEG.append(tuple(label[0]))
                elif label[2] == 'NEU':
                    NEU.append(tuple(label[0]))
            if not set(POS) & set(NEG) and not set(POS) & set(NEU) and not set(NEG) & set(NEU)  :
                load_data.append(f'{title}####{label_text}')

    train_data = sample(load_data, int(0.8*0.7*len(load_data)))
    eval_data = sample(load_data, int(0.8*0.3*len(load_data)))
    test_data = sample(load_data, int(0.2*len(load_data)))
    
    f = open('./processed_data/train_triplets.txt', 'w')
    for i in train_data:
        if i == train_data[len(train_data)-1]:
            f.write(f'{i}')
        else:
            f.write(f'{i}\n')

    f.close()

    f = open('./processed_data/dev_triplets.txt', 'w')
    for i in eval_data:
        if i == eval_data[len(eval_data)-1]:
            f.write(f'{i}')
        else:
            f.write(f'{i}\n')

    f.close()

    f = open('./processed_data/test_triplets.txt', 'w')
    for i in test_data:
        if i == test_data[len(test_data)-1]:
            f.write(f'{i}')
        else:
            f.write(f'{i}\n')

    f.close()

if __name__ == '__main__':
    main()