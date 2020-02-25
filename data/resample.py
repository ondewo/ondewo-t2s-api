import os
import json
from typing import List, Dict, Any
from multiprocessing import Pool

def resample(sample):
    filename = sample['audio_filepath']
    filename2 = filename.replace('ramona_deininger', 'ramona_deininger_2')
    os.system("sox " + filename  + " --bits 16 --endian little --channels 1 --encoding signed-integer --rate 22050 --type wav " + filename2)

def main():

    dataset_tr = "ramona_train.json"
    dataset_ts = "ramona_test.json"

    sample_list: List[Dict[str, Any]] = []

    with open(dataset_tr, "r") as d_file:
        for line in d_file:
            sample_list.append(json.loads(line))
    with open(dataset_ts, "r") as d_file:
        for line in d_file:
            sample_list.append(json.loads(line))
    
    pool = Pool()
    pool.map(resample, sample_list)

if __name__ == "__main__":
    main()
