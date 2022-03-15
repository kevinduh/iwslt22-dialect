#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quick script for computing WER and CER for IWSLT'22 using SCLITE
Usage:
  python3 wer_cer.py ref.txt hyp.txt tmp_path sclite_path

  ref.txt and hyp.txt are plain text files for reference and hypotheses, one utterance per line (no utterance id needed)
  sclite_path specifies location to sclite binary in https://github.com/usnistgov/SCTK install
  tmp_path specifies path where new temporary ref and hyp files will be created, in the format expected by sclite

  Written by Kevin Duh, with help from Ahmed Ali and Kenton Murray
"""

import sys
import os
import re
from datetime import datetime

ref=sys.argv[1]
hyp=sys.argv[2]
tmppath=sys.argv[3]
sclite=sys.argv[4]

#Keep only Arabic and Numbers and Space:
arabic_and_number=re.compile('[^اأإآبتثجحخدذرزسشصضطظعغفقكلمنهويىئءؤة0-9 ]')

#Further normalization:
_preNormalize = u" \u0629\u0649\u0623\u0625\u0622"
_postNormalize = u" \u0647\u064a\u0627\u0627\u0627"
_toNormalize = {ord(b):a for a,b in zip(_postNormalize,_preNormalize)}

def normalizeText(s):
    return arabic_and_number.sub('', s).translate(_toNormalize)

def write_line(filehandle, line, count):
    filehandle.write("%s (spk_%d)\n" %(line,count))

def process_file(filename, outprefix):
    original_words_file = open(outprefix + '.original_words', mode='w', encoding='UTF-8')
    normalized_words_file = open(outprefix + '.normalized_words', mode='w', encoding='UTF-8')
    original_chars_file = open(outprefix + '.original_chars', mode='w', encoding='UTF-8')
    normalized_chars_file = open(outprefix + '.normalized_chars', mode='w', encoding='UTF-8')
    with open(filename, mode='r', encoding='UTF-8') as F:
        for count, line in enumerate(F):
            original_words = line.rstrip()
            normalized_words = normalizeText(original_words)
            original_chars = ' '.join(original_words.replace(' ','▁'))
            normalized_chars = ' '.join(normalized_words.replace(' ','▁'))

            write_line(original_words_file, original_words, count)
            write_line(normalized_words_file, normalized_words, count)
            write_line(original_chars_file, original_chars, count)
            write_line(normalized_chars_file, normalized_chars, count)

    original_words_file.close()
    normalized_words_file.close()
    original_chars_file.close()
    normalized_chars_file.close()



def get_sclite_result(sclite_output_file, label):
    with open(sclite_output_file) as FID:
        for line in FID:
            if line.lstrip().startswith('| Sum/Avg|'):
                results = line.split()
                #num_sentence = results[2]
                num_token = results[3]
                #correct = results[5]
                #substitute = results[6]
                #deletion = results[7]
                #insertion = results[8]
                err_rate = results[9]
                print("%s: #hyp_token= %s error_rate= %s"%(label, num_token,err_rate))
                break

# step 1. write out files needed for sclite
print(hyp, datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
process_file(ref, tmppath+'.ref')
process_file(hyp, tmppath+'.hyp')

# step 2a. run sclite for wer on original version
os.system(f'{sclite} -r {tmppath}.ref.original_words trn -h {tmppath}.hyp.original_words trn -i rm -o sum stdout > {tmppath}.original.wer')
get_sclite_result(f'{tmppath}.original.wer', 'WER on original hypothesis')

# step 2b. run sclite for wer on normalized version
os.system(f'{sclite} -r {tmppath}.ref.normalized_words trn -h {tmppath}.hyp.normalized_words trn -i rm -o sum stdout > {tmppath}.normalized.wer')
get_sclite_result(f'{tmppath}.normalized.wer', 'WER on additionally-normalized hypothesis')

# step 3a. run sclite for cer on original version
os.system(f'{sclite} -r {tmppath}.ref.original_chars trn -h {tmppath}.hyp.original_chars trn -i rm -o sum stdout > {tmppath}.original.cer')
get_sclite_result(f'{tmppath}.original.cer', 'CER on original hypothesis')

# step 3b. run sclite for cer on normalized version
os.system(f'{sclite} -r {tmppath}.ref.normalized_chars trn -h {tmppath}.hyp.normalized_chars trn -i rm -o sum stdout > {tmppath}.normalized.cer')
get_sclite_result(f'{tmppath}.normalized.cer', 'CER on additionally-normalized hypothesis')



