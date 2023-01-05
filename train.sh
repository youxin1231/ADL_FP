script_dir=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd "$script_dir"

if [ ! -d "./processed_data" ]; then
    mkdir processed_data
fi

python3 src/preprocess.py

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