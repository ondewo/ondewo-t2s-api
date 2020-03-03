"""Script for normalizing and cleaning data in NeMo format.

The script takes NeMo-formated JSON dataset as input.
It does the following:
1. normalizes text (removes punctiation, lowercase letters)
2. checks if all paths are actual files, removes them from JSON if they aren't
3. checks if all transcriptions have >=3 characters, removes them if they have less 
4. (optional, deep) gets actual file duration, checks if it is between 0.5 and 20 seconds long.
5. (optional, deep) checks if the sampling rate is 22050 Hz
6. (optional, deep) checks that not more than 50 characters are spoken per second (also, CTC loss will be infinite in this case)
)
7. (optional, deep) removed all transciption which are over 180 character long

"""
import argparse
import json
import string
from typing import Dict, List, Any
from os.path import isfile
import soundfile as sf


def main():
    # parse arguments
    parser = argparse.ArgumentParser(description='Script for normalizing and cleaning data in NeMo format.')
    parser.add_argument("-d", type=str, help="Dataset in the NeMo format.")
    parser.add_argument("-c", type=str, help="Filename for the normalized dataset.")
    parser.add_argument("--deep", type=str, default=False, help="Read wav header to check duration and sampling rate")
    args = parser.parse_args()
    dataset: str = args.d

    sample_list: List[Dict[str, Any]] = []
    with open(dataset, "r") as d_file:
        for line in d_file:
            sample_list.append(json.loads(line))

    cleaned_sample_list: List[Dict[str, Any]] = []
    removed_samples_counter: int = 0
    for sample in sample_list:

        # normalize text
        sample['text'] = normalize_text(sample['text'])
        
        # checks if audiofile path is an actual file
        if not isfile(sample['audio_filepath']):
            print("Found corrupted sample - missing audiofile.")
            removed_samples_counter += 1
            continue
        
        # checks if transcription is less than 3 characters.
        if len(sample['text']) < 3:
            print("Found bad sample - less than 3 chars.")
            removed_samples_counter += 1
            continue

        if args.deep:
            f = sf.SoundFile(sample['audio_filepath'])
            
            if f.samplerate != 22050:
                print("Found bad sample - wrong samplerate.")
                removed_samples_counter += 1
                continue 

            duration: float = len(f) / f.samplerate
            if duration < 0.5:
                print("Found bad sample - less than 0.5 seconds.")
                removed_samples_counter += 1
                continue
                
            if duration > 20:
                print("Found bad sample - longer than 20 seconds.")
                removed_samples_counter += 1
                continue

            if len(sample['text']) > duration * 50:
                print("Found bad sample - more than 50 chars a second")
                removed_samples_counter += 1
                continue

            if len(sample['text']) > 180:
                print("Found bad sample - more than 180 chars in transcipt.")
                removed_samples_counter += 1
                continue

            sample['duration'] = duration

        cleaned_sample_list.append(sample)

    print("In total: from original " + str(len(sample_list)) + \
        " samples, found " + str(removed_samples_counter) + \
        " bad samples.")
    write_json_to_file(cleaned_sample_list, args.c)


def normalize_text(text: str) -> str:
    """Perform text normalization.

    Returns: normalized text

    """
    text = text.lower()

    # https://stackoverflow.com/questions/265960/best-way-to-strip-punctuation-from-a-string-in-python
    table = str.maketrans({key: None for key in string.punctuation})
    text = text.translate(table)

    return text


def write_json_to_file(sample_list: List[Dict[str, Any]], filename: str):
    with open(filename, 'w') as outfile:
        for sample in sample_list:
            sample_s = json.dumps(sample)
            outfile.write(sample_s)
            outfile.write('\n')

if __name__ == "__main__":
    main()
