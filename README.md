# Forum Understanding Using NLP Techniques

## Hardware
- CPU: AMD 7950X
- GPU: RTX 2080ti

## Enviroment
It's recommand to create a virtual enviroment, e.g. conda.

```shell
pip install -r requirements.txt
```

## Download
To download the fine-tuned models for reproducing.
```shell
bash download.sh
```

## Reproduce

### Train
To preporcess the data and training.
- Running shell script.
```shell
bash train.sh
```
or

- And here is how you would use it on your own files, after adjusting the values for the arguments `--train_path`, `--dev_path` to match your setup

- You could also setting different hyperameters by adjusting the values for the arguments `--learning_rate` , `--num_epochs`

```shell
python3 src/span-aste/train.py \
    --batch_size 1 \
    --learning_rate 5e-5 \
    --weight_decay 1e-2 \
    --warmup_proportion 0.1 \
    --train_path processed_data \
    --dev_path processed_data \
    --ckpt_dir ckpt/span-aste \
    --output_dir output \
    --max_seq_len 256 \
    --num_epochs 70 \
    --seed 2022 \
    --logging_steps 480 \
    --valid_steps 480 \
    # --init_from_ckpt \
```

### Test

1. Sentiment analysis
- Running shell script.
```shell
bash test.sh
```

or 

- You could also setting different parameter in `--test_path` to save the output in other location.

```shell
python3 src/span-aste/test.py \
    --test_path processed_data \
    --ckpt ckpt/span-aste \
    --output_dir output \
```

2. Topic model
- Executing `.ipynb` files in /src/Bertopic
- Name of the file represent the test data crawl from which topic on Reddit.
    
