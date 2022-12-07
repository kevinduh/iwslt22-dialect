#!/usr/bin/env python3

"""
The original file LDC2022E02/data/segments.txt contains 4293 lines.
Among these, 5 lines are actually bad segments, and should be filtered. 
If you decoded with the original segments file and generated 
transcriptions/translations with 4293 lines, run this script to 
filter out the 5 bad lines. The result will be a output with 4288 lines.
These bad segments correspond to zero duration or no speech. 

(script by Kevin Duh, for IWSLT'22, 3/23/2022)
"""

import sys

# path to LDC2022E02/data/segments.txt
original_segments_file = sys.argv[1] 

# file to filter, should be 4293 lines 
file_to_filter = sys.argv[2]

# resulting filtered line, should be 4288 lines
resulting_file = sys.argv[3]


bad_segment = set(['20170606_000110_13802_A_008209-008322 20170606_000110_13802_A 82.098 83.220',
                   '20170606_000110_13802_A_010606-010757 20170606_000110_13802_A 106.060 107.570',
                   '20170606_000110_13802_B_039745-039907 20170606_000110_13802_B 397.450 399.078',
                   '20170606_000110_13802_B_053041-053104 20170606_000110_13802_B 530.410 531.040',
                   '20170907_204736_16787_A_040194-040194 20170907_204736_16787_A 401.944 401.944'])

line_number = set()
with open(original_segments_file) as F:
    for i, line in enumerate(F):
        if line.rstrip() in bad_segment:
            line_number.add(i)
            
count = 0
with open(file_to_filter, mode='r', encoding='utf-8') as INFILE, open(resulting_file, mode='w', encoding='utf-8') as OUTFILE:
    for i, line in enumerate(INFILE):
        if i in line_number:
            print("Skip line %d: %s" %(i, line), end='')
        else:
            OUTFILE.write(line)
            count += 1

assert(count==4288)
