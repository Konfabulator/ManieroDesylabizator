import os, sys    
os.chdir(os.path.dirname(os.path.abspath(__file__)))
cwd = os.getcwd()
if sys.platform == "win32":
    sys.path.append(cwd[:cwd.rfind("\\")])
else:
    sys.path.append(cwd[:cwd.rfind("/")])
    
import numpy as np
import json 
import random

# open files
# words_with_sylabes_file = open('words_with_sylabes.txt', 'r', encoding='utf-8') # "word":"sylabe-sylabe-sylabe"
words_with_sylabes_file = open('expert_set.txt', 'r', encoding='utf-8') # "word":"sylabe-sylabe-sylabe"
training_set_file = open('training_set_expert.txt', 'w', encoding='utf-8')     # "sentence":[list of one_hot_enc(sylabe)]

# load files
words_with_sylabes = { line.strip().split()[0]:line.strip().split()[1:] for line in words_with_sylabes_file}
wws_words = list(words_with_sylabes.keys())
wws_sylabes = list(words_with_sylabes.values())
len_words = len(words_with_sylabes)

# close files
words_with_sylabes_file.close()

# generate training set
training_set = {}

print('Generating training set...')

# create training set of 100000 sentences - each of random (1-10) words 
N = len(words_with_sylabes)
m = N//100

max_length = 32
def converter(socations, max_len):
    one_hot_enc = [0]*max_len
    for loc in socations:
        one_hot_enc[loc] = 1
    return one_hot_enc

for i in range(N):
    sylabes_in_sentence = []
    n = i#random.randint(0,len(words_with_sylabes)-1)
    word = wws_words[n]
    sylabes_in_word = wws_sylabes[n]
    # get localisation of sylabes in word
    sylabes_in_word_localisation = [0]
    for sylabe in sylabes_in_word:
        sylabes_in_word_localisation.append(sylabes_in_word_localisation[-1] + len(sylabe))
    # add sylabes to sentence
    sylabes_in_sentence = [loc+len(sylabes_in_sentence) for loc in sylabes_in_word_localisation[:-1]]
    # training_set[word] = sylabes_in_sentence
    
    training_set_file.write(word + ' ' + ' '.join(map(str, converter(sylabes_in_sentence, max_length))) + '\n')
    if i % m == 0:
        # print('Sentence', i, 'of\t', N, end="\r")
        # print('Done', 100*i/N, '%', end="\r")
        # two decimal places
        print('Done', "{:.3f}".format(100*i/N), '%', end="\r")
        training_set_file.flush()

print('Done generating training set')
training_set_file.close()


# for sentence, sylabes in training_set.items():
#     training_set_file.write(sentence + ' ' + ' '.join(map(str, converter(sylabes, max_length))) + '\n')
