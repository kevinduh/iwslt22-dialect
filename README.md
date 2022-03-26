# IWSLT 2022 Dialectal Speech Translation Task 

## Scripts for data preparation

First, obtain the Tunisian-English Speech Translation data (LDC2022E01) from LDC, following the instructions on the <a href="https://iwslt.org/2022/dialect">shared task website</a>.

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


## Scripts for BLEU evaluation

We will use <a href="https://github.com/mjpost/sacrebleu">SacreBLEU</a> for evaluation of speech translation output. The following shows how we would compute (lowercased) BLEU on a detokenized example output (`example/example.st.unconstrained.contrastive1.aeb-eng.txt`):

```
pip install sacrebleu==2.0.0
cut -f 7- stm/st-aeb2eng.norm.test1.stm > example/test1.reference.eng
sacrebleu example/test1.reference.eng -i example/example.st.unconstrained.contrastive1.aeb-eng.txt -m bleu -lc
``` 

This should give:
```
{
 "name": "BLEU",
 "score": 19.1,
 "signature": "nrefs:1|case:lc|eff:no|tok:13a|smooth:exp|version:2.0.0",
 "verbose_score": "50.8/26.0/13.9/7.7 (BP = 0.985 ratio = 0.985 hyp_len = 41561 ref_len = 42181)",
 "nrefs": "1",
 "case": "lc",
 "eff": "no",
 "tok": "13a",
 "smooth": "exp",
 "version": "2.0.0"
}
```

## Scripts for WER/CER evaluation

We'll compute WER and CER for ASR outputs as follows, using the SCLITE tool: 
```
python3 ./wer_cer.py example/smallset.reference.aeb example/smallset.asr.unconstrained.contrastive1.aeb.txt tmp ~/sctk/bin/sclite
```

This should give something like the following (Note this example may not be representative of actual WER/CER because it's just a small set of 100 utterances):
```
example/smallset.asr.unconstrained.contrastive1.aeb.txt 25/03/2022 22:49:38
WER on original hypothesis Error_Rate= 37.5 (#snt=100 #token=600 Corr=67.3 Sub=26.0 Del=6.7 Ins=4.8)
WER on additionally-normalized hypothesis Error_Rate= 31.7 (#snt=100 #token=600 Corr=73.2 Sub=20.2 Del=6.7 Ins=4.8)
CER on original hypothesis Error_Rate= 18.7 (#snt=100 #token=3116 Corr=88.1 Sub=4.7 Del=7.3 Ins=6.8)
CER on additionally-normalized hypothesis Error_Rate= 16.8 (#snt=100 #token=2921 Corr=89.3 Sub=3.7 Del=7.1 Ins=6.1)
```

The WER/CER on "original" refers to text like `asr-aeb.norm.stm` as provided by the setup_data.sh (not the `asr-aeb.raw.stm`). 
The WER/CER on "additionally-normalized" underwent additional normalization (not provided by setup_data.sh) and includes things like diacritic removal (see wer-cer.py for full set of additional normalization). Multiple versions are provided only as diagnostic. 

