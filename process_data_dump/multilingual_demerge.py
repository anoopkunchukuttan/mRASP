import argparse
import os
import sys 
from collections import defaultdict

def read_pc32corpus(sfname, tfname):
    with open(sfname, 'r', encoding='utf-8') as sf, \
         open(tfname, 'r', encoding='utf-8') as tf:    
         for n, (sline, tline) in enumerate(zip(sf,tf)):
            yield(sline.strip(), tline.strip())



def multilingual_demerge(sfname, tfname, outdir, dset): 
    """
    This function demerges the multilingual data into separate files for each language.
    """
    # dictionary of open files for writing 
    # {
    #   'en-de': {
    #                'en': <file object>,  
    #                'de': <file object>,
    #             },
    # }
    pcdict=defaultdict(dict)

    for sline, tline in read_pc32corpus(sfname, tfname):
        slang_tok=sline.strip().split(' ')[0]
        tlang_tok=tline.strip().split(' ')[0]

        # get third column of s
        slang=slang_tok.split('_')[2].lower()
        tlang=tlang_tok.split('_')[2].lower()

        # get the language pair
        lang_pair=slang+'-'+tlang
        # check if the language pair is in the parallel corpus dictionary   
        if lang_pair not in pcdict:
            # create a new language pair
            pcdict[lang_pair]={}
            pair_dir=f'{outdir}/{lang_pair}'
            os.makedirs(pair_dir, exist_ok=True)
            prefix=f'{pair_dir}/{dset}'
            # create a new source file
            pcdict[lang_pair][slang]=open(f'{prefix}.{slang}','w', encoding='utf-8')
            # create a new target file
            pcdict[lang_pair][tlang]=open(f'{prefix}.{tlang}','w', encoding='utf-8')

        # write the source and target lines to the respective files. Only extract the text and not the language id
        pcdict[lang_pair][slang].write(' '.join(sline.strip().split(' ')[1:])+'\n')
        pcdict[lang_pair][tlang].write(' '.join(tline.strip().split(' ')[1:])+'\n')

    ## close all the open files 
    for lang_pair in pcdict:
        for lang in pcdict[lang_pair]:
            pcdict[lang_pair][lang].close()      

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', type=str, required=True)
    parser.add_argument('-t', type=str, required=True)
    parser.add_argument('-o', type=str, required=True)
    parser.add_argument('-d', type=str, required=True)  

    args = parser.parse_args()
    multilingual_demerge(args.s, args.t, args.o, args.d)                  

