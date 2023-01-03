#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# ====================================
# @Project ：insights-span-aste
# @IDE     ：PyCharm
# @Author  ：Hao,Wireless Zhiheng
# @Email   ：hpuhzh@outlook.com
# @Date    ：05/08/2022 9:57 
# ====================================
import argparse
import os

import pandas as pd
import torch
from torch.utils.data import DataLoader
from transformers import BertTokenizer
from models.collate import collate_fn
from models.model import SpanAsteModel
# from trainer import SpanAsteTrainer
from utils.dataset import CustomDataset
from utils.tager import SpanLabel, RelationLabel
import json
import re
from pathlib import Path

def main(args):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    print(f"using device:{device}")
    # tokenizer
    tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")

    print("Building SPAN-ASTE model...")
    # get dimension of target and relation
    target_dim, relation_dim = len(SpanLabel), len(RelationLabel)
    # build span-aste model
    model = SpanAsteModel(
        "bert-base-uncased",
        target_dim,
        relation_dim,
        device=device
    )

    model.load_state_dict(torch.load(os.path.join(args.ckpt, "model.pt"), map_location=torch.device(device)))
    model.to(device)
    model.eval()

    with open(f'{args.test_path}/test_triplets.txt', "r", encoding="utf8") as f:
        data = f.readlines()
    res = []
    for d in data:
        text, label = d.strip().split("####")

        tokens = ["[CLS]"] + tokenizer.tokenize(text) + ["[SEP]"]

        input = tokenizer(text, max_length=128, padding=True, truncation=True, return_tensors="pt").to(device)

        input_ids = input.input_ids
        attention_mask = input.attention_mask
        token_type_ids = input.token_type_ids
        seq_len = (input_ids != 0).sum().item()

        # forward
        spans_probability, span_indices, relations_probability, candidate_indices = model(
            input_ids, attention_mask, token_type_ids, [seq_len])

        relations_probability = relations_probability.squeeze(0)
        predict = []
        for idx, can in enumerate(candidate_indices[0]):
            a, b, c, d = can
            aspect = tokenizer.convert_tokens_to_string(tokens[a:b])
            opinion = tokenizer.convert_tokens_to_string(tokens[c:d])
            sentiment = RelationLabel(relations_probability[idx].argmax(-1).item()).name

            if sentiment != RelationLabel.INVALID.name:
                predict.append((aspect, opinion, sentiment))
        print("text:", text)
        print("predict", predict)
        labels = []
        words = text.split(" ")
        for l in eval(label):
            a, o, sm = l
            a = " ".join([words[i] for i in a])
            o = " ".join([words[i] for i in o])
            labels.append((a, o, sm))
        print("label", labels)
        if len(predict) != 0:
            res.append({"text": text, "predict": predict, "label": labels})

    # dataframe = pd.DataFrame(res)
    # dataframe.to_excel("output.xlsx")

    posts = pd.DataFrame(res,columns=['text','predict','label'])
    result = posts.to_json(orient="records")
    parsed = json.loads(result)

    json_object = json.dumps(parsed, indent=4, ensure_ascii=False)
    # json_object = re.sub(r'",\s+', '", ', json_object)

    outfile = Path(args.output_dir / 'span-aste.json')
    outfile.write_text(json_object, encoding='UTF-8')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("--test_path", default="processed_data", type=str, help="The path of test set.")
    parser.add_argument("--ckpt", default='ckpt/span-aste', type=str,
                        help="The path of model parameters for initialization.")
    parser.add_argument("--output_dir", default="output", type=Path, help="The path of output folder.")
    
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    main(args)