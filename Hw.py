# -*- coding: utf-8 -*-
"""
Created on Sun Oct  4 17:54:35 2015

@author: Szabolcs
"""

import argparse

def add_word_to_dictionary(word: str, dictionary: dict):
    if not word:
        dictionary['is_word'] = True
        return
    if word[0] not in dictionary:
        dictionary[word[0]] = {'is_word': False}
    add_word_to_dictionary(word[1:], dictionary[word[0]])
    
def word_is_in_dictionary(word: str, dictionary: dict):
    if not word:
        return dictionary.get('is_word', False)
    if word[0] not in dictionary:
        return False
    return word_is_in_dictionary(word[1:], dictionary[word[0]])
    
class Parser():
    def __init__(self, dictionary):
        self._dictionary = dictionary

    def get_first_key_word_from_line(self, line: list):
        if not line:
            return ""
        if word_is_in_dictionary(line[0].strip(), self._dictionary):
            return line[0].strip()
        return self.get_first_key_word_from_line(line[1:])
    

def line_reader(file_path: str):
    with open(file_path, "r", encoding="utf8") as f:
        for line in f:
            yield line 
    
def save_to_file(name, content):
    if name:
        with open("../{name}.txt".format(name=name), "a", encoding="utf8") as f:
            f.write(content)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Log processor')
    parser.add_argument('--dictionary', type=str, dest='dict_path',
                        help='contains wich words want to matched in log')
    parser.add_argument('--log-file', type=str, dest='log_path', 
                        help='path of the parseble log')

    args = parser.parse_args()
    dictionary = {}
    for word in line_reader(args.dict_path):
        add_word_to_dictionary(word.strip(), dictionary)
    
    parser = Parser(dictionary)
    for line in line_reader(args.log_path):
        save_to_file(parser.get_first_key_word_from_line(line.split()), line)
    
    