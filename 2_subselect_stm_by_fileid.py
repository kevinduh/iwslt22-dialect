#!/usr/bin/env python3

import argparse
import os

def parse_input():
    parser = argparse.ArgumentParser("Subselects STM based on a list of fileid, to create train/dev splits")
    parser.add_argument("--stm-in", help="Input STM")
    parser.add_argument("--stm-out", help="Output STM")
    parser.add_argument("--fileid", help="e.g. train.file_id.txt")
    parser.add_argument("--audiopath", help="full path to audio file directory")
    parser.add_argument("--audiosuffix", help="audio filename extension", default='.sph')
    args = parser.parse_args()
    return args 

def main():
    args = parse_input()

    with open(args.fileid, 'r') as FILEIDLIST:
        selected=set(FILEIDLIST.read().splitlines())

    with open(args.stm_in, 'r', encoding='utf-8') as INFILE, open(args.stm_out, 'w', encoding='utf-8') as OUTFILE:
        for line in INFILE:
            fields = line.split('\t')
            fileid = fields[0]
            fields[0] = os.path.join(args.audiopath, fileid + args.audiosuffix)
            if fileid in selected:
                OUTFILE.write("\t".join(fields))


if __name__ == "__main__":
    main()