#!/usr/bin/env python3

import sys
import os
import argparse
import glob
import re
from collections import defaultdict


# English annotation rules:
# -------------------------------
#     (()) - Uncertain word or words
#      %pw - Partial word
#       #  - Foreign word, either followed by translation or (()) if cannot translate
#       +  - Mis-pronounced word (carried over from mispronunciation marked in transcript)
#      uh, um, eh or ah - Filled pauses
#       =  - Typographical error from transcript


# Arabic annotation rules:
# -------------------------------
# O/ - foreign
# U/ - uncertain
# M/ - MSA
# UM/ - uncertain + MSA
# UO/ - uncertain + foreign

arabic_filter = re.compile(r'[OUM]+/*|\u061F|\?|\!|\.')
english_filter = re.compile(r'\(|\)|\#|\+|\=|\?|\!|\;|\.|\,|\"|\:')


def parse_input():
    parser = argparse.ArgumentParser("Creates STM from LDC2022E01 distribution")
    parser.add_argument("--LDC2022E01", help="root of LDC distribution")
    parser.add_argument("--stm-dest", 
                        help="destination directory to be created for output files")
    parser.add_argument("--exclude", help="predefined list of faulty utterances to exclude")
    args = parser.parse_args()
    return args 


def normalize_text(utterance, language):
    if language == "<aeb>":
        return re.subn(arabic_filter, '', utterance)[0]
    elif language == "<eng>":
        return re.subn(english_filter, '', utterance)[0].lower()
    else:
        raise ValueError(f'Text normalization for {language} is not supported')  
        

def prepare_stm(root, stm, label, exclude_utterance):

    # stores all utterances, to be sorted before output: all_utterances[fileid][starttime] -> utterance, etc.
    all_utterances = defaultdict(lambda: defaultdict(list))

    # collect character histogram statistics: char_histogram['char']['{raw,norm}'] -> count
    char_histogram = defaultdict(lambda: defaultdict(int))

    # loop over each TSV file
    for tsvfile in glob.glob(root + "/*.tsv", recursive=False):
        with open(tsvfile, encoding='utf-8') as TSV:
            fileid = os.path.basename(tsvfile).split('.')[0]
            channelid = '1'
            for line in TSV:
                starttime, endtime, speakerid, utterance = line.rstrip().split('\t')
                if f"{fileid} {starttime} {endtime}" not in exclude_utterance:
                    normalized_utterance = normalize_text(utterance, label)
                    metainfo = f"{fileid}\t{channelid}\t{speakerid}\t{starttime}\t{endtime}\t{label}"
                    all_utterances[fileid][float(starttime)] = [metainfo, utterance, normalized_utterance]

    # save two sorted STM file, raw version is original text, norm version applies normalization
    with open(stm+'.raw.stm', 'w') as STM_RAW, open(stm+'.norm.stm', 'w') as STM_NORM:
        for fileid in sorted(all_utterances):
            for starttime in sorted(all_utterances[fileid]):
                u=all_utterances[fileid][starttime]
                print("%s\t%s" %(u[0],u[1]), file=STM_RAW)
                print("%s\t%s" %(u[0],u[2]), file=STM_NORM)
                for c in u[1]: char_histogram[c]['raw'] += 1
                for c in u[2]: char_histogram[c]['norm'] += 1

    # save character histogram for diagnostics
    with open(stm+'.char_histogram', 'w') as CHAR_HIST:
        print("#character count_in_raw count_in_norm count_equal?", file=CHAR_HIST)
        for c, counts in sorted(char_histogram.items(), key=lambda kv:kv[1]['raw'], reverse=True):
            print("%s %d %d %s" %(c, counts['raw'], counts['norm'], counts['raw'] == counts['norm']), file=CHAR_HIST)


def main():
    args = parse_input() 

    os.makedirs(args.stm_dest, exist_ok=True)
    exclude_utterance = set(line.strip() for line in open(args.exclude))

    prepare_stm(
        os.path.join(args.LDC2022E01,'data/translations/ta'),
        os.path.join(args.stm_dest,'st-aeb2eng'),
        '<eng>', exclude_utterance
    )

    prepare_stm(
        os.path.join(args.LDC2022E01,'data/transcripts/ta'),
        os.path.join(args.stm_dest,'asr-aeb'),
        '<aeb>', exclude_utterance
    )



if __name__ == "__main__":
    main()
    
