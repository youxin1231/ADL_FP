if [ ! -d "./processed_data" ]; then
    mkdir processed_data
fi
python3 src/preprocess.py
# python3 src/SBN/run.py