#!/bin/bash
#INPUT=~/donkey-data/data/tammerforce-newcar-train
INPUT=~/donkey-data/data/tammerforce-newcar-train-processed
#WORKING_DIR=~/donkey-data/data/tammerforce-augmented-set
WORKING_DIR=~/donkey-data/data/tammerforce-augmented-processed-set

# Pass 1: flip
FLIP_OUTPATH=${WORKING_DIR}/flipped
mkdir ${FLIP_OUTPATH}
python ./util/augment.py --path $INPUT --out $FLIP_OUTPATH --aug=flip

# Pass 2: Brightness
BRIGHT_OUTPATH=${WORKING_DIR}/brightness
mkdir ${BRIGHT_OUTPATH}
python ./util/augment.py --path $INPUT --out $BRIGHT_OUTPATH --aug=bright
python ./util/augment.py --path $FLIP_OUTPATH --out $BRIGHT_OUTPATH --aug=bright


