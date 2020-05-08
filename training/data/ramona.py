import argparse
import json
import string
from typing import Dict, List, Any
import random

def main():
    test_dataset = 'mailabs_cleaned_test_2.json'
    train_dataset = 'mailabs_cleaned_train_2.json'

    test_list: List[Dict[str, Any]] = []
    with open(test_dataset, "r") as d_file:
        for line in d_file:
            test_list.append(json.loads(line))
    train_list: List[Dict[str, Any]] = []
    with open(train_dataset, "r") as d_file:
        for line in d_file:
            train_list.append(json.loads(line))

    train_list_tts: List[Dict[str, Any]] = []
    test_list_tts: List[Dict[str, Any]] = []

    for sample in train_list:
        if 'ramona_deininger' in sample['audio_filepath']:
            sample['audio_filepath'] = sample['audio_filepath'].replace('/opt/nemo_v/data/mailabs/raw/by_book/female/', '/opt/stella/data/')
            train_list_tts.append(sample)
    for sample in test_list:
        if 'ramona_deininger' in sample['audio_filepath']:
            sample['audio_filepath'] = sample['audio_filepath'].replace('/opt/nemo_v/data/mailabs/raw/by_book/female/', '/opt/stella/data/')
            test_list_tts.append(sample)
    
    write_json_to_file(train_list_tts, 'ramona_train.json')
    write_json_to_file(test_list_tts, 'ramona_test.json')


def write_json_to_file(sample_list: List[Dict[str, Any]], filename: str):
    with open(filename, 'w') as outfile:
        for sample in sample_list:
            sample_s = json.dumps(sample)
            outfile.write(sample_s)
            outfile.write('\n')

if __name__ == "__main__":
    main()
