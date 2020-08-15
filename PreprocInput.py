import os
import sys

curruser = os.environ.get('USER')
sys.path.insert(0, '/home/{}/.local/lib/python3.6/site-packages/'.format(curruser))

import re
from tqdm import tqdm
import pandas as pd
import numpy as np
from textwrap import wrap
import random

class preproc_(object):
    
    def __init__(self):
        pass
    
    def get_wrap_chunks(seq_list, min_seq_len, max_seq_len):
        new_seq = []
        for seq in seq_list:
            if len(seq) <= max_seq_len+1  & len(seq) >= min_seq_len+1:
                new_seq.append(seq)
            elif len(seq) < min_seq_len+1:
                pass
            else:
                chunks = wrap(seq, max_seq_len+1)
                for i in chunks:
                    if len(i) >= min_seq_len+1:
                        new_seq.append(i)
                    else:
                        pass

        return new_seq
    
    def get_chunks_FromLeftToRight(seq_list, min_seq_len, max_seq_len, step):
        sequences = []
        next_char = []
        for seq in seq_list:
            for LenSeq in range(min_seq_len, max_seq_len+1, 1):
                for i in range(0, len(seq) - LenSeq, step):
                    sequences.append(seq[i: i + LenSeq])
                    next_char.append(seq[i + LenSeq])

        return sequences, next_char

    def get_input_array(seq_list, label_list, max_seq_len, vocab, char_ind_vocab):
        X_data = np.zeros((len(seq_list), max_seq_len, len(vocab)), dtype=np.bool)
        y_data = np.zeros((len(seq_list), len(vocab)), dtype=np.bool)
        for i, sentence in enumerate(seq_list):
            for t, char in enumerate(sentence):
                X_data[i, t, char_ind_vocab[char]] = 1
            y_data[i, char_ind_vocab[label_list[i]]] = 1
            
        return X_data, y_data
    
    def RandSample(min_len, max_len, seqArr, size):
        sequences=[]
        next_char=[]
        seq_list = np.random.choice(seqArr, size)
        for seq in seq_list:
            len_ = random.randint(min_len,max_len)
            if len(seq) >= len_*2+1:
                step = random.randint(0,len(seq)-len_*2+1)
                sequences.append(''.join([seq[step:step+len_],seq[step+len_+1:step+len_*2+1]]))
                next_char.append(seq[step+len_]) 
            else:
                pass
        return sequences, next_char
    
    def RandSample_withcenter(min_len, max_len, seqArr, size):
        sequences=[]
        next_char=[]
        seq_list = np.random.choice(seqArr, size)
        for seq in seq_list:
            len_ = random.randint(min_len,max_len)
            if len(seq) >= len_+1:
                step = random.randint(0,len(seq)-len_-1)
                sequences.append(seq[step:step+len_])
                next_char.append(seq[step+len_]) 
            else:
                pass
        return sequences, next_char