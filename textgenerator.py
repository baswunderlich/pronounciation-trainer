import os
from os import listdir
from os.path import isfile, join
import random
import math

symbols = [".", ",", "-", "!", "?", "_", "\"", "'"]
current_text = ""

def get_new_text(mode) -> str:
    current_text = get_random_text_chunk(mode)
    return current_text

def get_random_text_chunk(mode = "default") -> (str, str):
    mypath = "texts/" + mode
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    chosen_file = random.choice(onlyfiles)
    with open(mypath + "/" + chosen_file, "r", encoding="utf-8") as file:
        sentences_count = 0
        full_text = file.read()
        full_text.find(".")
        sentence_indexes = [i for i in range(len(full_text)) if full_text.startswith('.', i)]
        
        starting_sentence = random.randint(0, len(sentence_indexes)-4)

        text = full_text[sentence_indexes[starting_sentence]+1: sentence_indexes[starting_sentence+3]]
        
        #
        return text

def clean_text(text) -> str:
    for symbol in symbols:
        text = text.replace(symbol, " ")
    return text.lower()
