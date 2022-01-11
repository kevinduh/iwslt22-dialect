# IWSLT 2022 Dialectal Speech Translation Task 

## Scripts for data preparation

First, obtain the Tunisian-English Speech Translation data (LDC2022E01) from LDC, following the instructions on the <a href="">shared task website</a>.

Then, clone this repo and run: 
```
git clone https://github.com/kevinduh/iwslt22-dialect.git
cd iwslt22-dialect/
/bin/sh setup_data.sh $datapath
```

Here,  `$datapath` points to location of the unzipped LDC2022E01 package on your filesystem. (For example, `$datapath=/home/corpora/LDC2022E01_IWSLT22_Tunisian_Arabic_Shared_Task_Training_Data/`)

This script reads from the LDC2022E01 package and generates several stm files in `iwslt22-dialect/stm`. 

```
wc -l stm/*stm
     3833 stm/asr-aeb.norm.dev.stm
   397699 stm/asr-aeb.norm.stm
     4204 stm/asr-aeb.norm.test1.stm
   202499 stm/asr-aeb.norm.train.stm
   397699 stm/asr-aeb.raw.stm
     3833 stm/st-aeb2eng.norm.dev.stm
   210536 stm/st-aeb2eng.norm.stm
     4204 stm/st-aeb2eng.norm.test1.stm
   202499 stm/st-aeb2eng.norm.train.stm
   210536 stm/st-aeb2eng.raw.stm
```

We will be using only the normalized files `*.norm.*.stm` during evaluation, and recommend that you use them for training too. 
The `*.raw.*.stm` files correspond to the original raw text and are not necessary; if interested, please refer to the python code `1_prepare_stm.py` (called by `setup.data.sh`) to see what is changed when going from raw to norm stm files (stripping symbols, lowercasing). 

Specifically, to build your systems for the basic condition, the files of interest are:

* Tunisian ASR: `stm/asr-aeb.norm.train.stm` for training, `stm/asr-aeb.norm.dev.stm` for development, `stm/asr-aeb.norm.test1.stm` for internal testing
* Tunisian-English E2E Speech Translation: `stm/st-aeb2eng.norm.train.stm` for training, `stm/st-aeb2eng.norm.dev.stm` for development, `stm/st-aeb2eng.norm.test1.stm` for internal testing 

We will provide a new blind test set (called `test2`) for official evaluation later. 

Note that LDC2022E01 also provides a small sample of Modern Standard Arabic files; if desired, you can treat this as a separate unofficial test set to compare with your Tunisian ASR/ST results.  

## STM File format

The STM Reference file format consists of several tab-separated fields per line

```
STM :== <F> <C> <S> <BT> <ET> text
where
<F> = filename of audio (sph file)
<C> = audio channel (channel=1 in all cases here)
<S> = speaker id
<BT> = begin time of utterance (seconds)
<ET> = end time of utterance
text = reference Arabic for asr-aeb.*.stm and reference English for st-aeb2eng.*.stm
```

The STM files can be used as input to, for example, Kaldi ASR's data processing <a href="https://github.com/kaldi-asr/kaldi/blob/master/egs/babel/s5/local/prepare_stm.pl">scripts</a>. For MT bitext, the n-th line of `stm/asr-aeb.norm.train.stm` is sentence-aligned to the same n-th line of `stm/st-aeb2eng.norm.train.stm`, and similarly for the `*.{dev,test1}.stm` files.


## Scripts for WER and BLEU evaluation

TBA