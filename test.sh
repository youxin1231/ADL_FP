script_dir=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd "$script_dir"

if [ ! -d "./processed_data" ]; then
    mkdir processed_data
fi

python3 src/preprocess.py

python3 src/span-aste/test.py \
    --test_path processed_data \
    --ckpt ckpt/span-aste \
    --output_dir output \