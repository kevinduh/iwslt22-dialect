#!/bin/sh

ldc_path=$1
#ldc_path=~/data/ldc/LDC2022E01

echo "1. Prepare STM"
./1_prepare_stm.py --LDC2022E01 ${ldc_path} --stm-dest stm --exclude exclude-utterance.txt

for task in asr-aeb.norm st-aeb2eng.norm ; do
    echo "2. Train/dev/test split for $task"
    for dset in dev test1 train ; do
        ./2_subselect_stm_by_fileid.py --stm-in stm/$task.stm --stm-out stm/$task.$dset.stm --fileid $dset.file_id.txt --audiopath ${ldc_path}/data/audio/ta
    done
done
