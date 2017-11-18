#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import sys
import os.path
import json
import hunspell

# spellchecker = hunspell.HunSpell('/usr/share/hunspell/en_US.dic', '/usr/share/hunspell/en_US.aff')
spellchecker = hunspell.HunSpell('./lib/dict/Russian.dic', './lib/dict/Russian.aff')

def correct_words(words, add_to_dict=[]):
    """
    Автокоррекция из словаря на 1 вариант
    https://datascience.blog.wzb.eu/2016/07/13/autocorrecting-misspelled-words-in-python-using-hunspell/
    """

    enc = spellchecker.get_dic_encoding()   # get the encoding for later use in decode()
    print (enc)

    # add custom words to the dictionary
    for w in add_to_dict:
        spellchecker.add(w)

    # auto-correct words
    corrected = []
    for w in words:
        ok = spellchecker.spell(w)   # check spelling
        if not ok:
            suggestions = spellchecker.suggest(w)
            print(json.dumps(suggestions,  sort_keys=True, ensure_ascii=False))
            if len(suggestions) > 0:  # there are suggestions
                # best = suggestions[0].decode(enc)
                best = suggestions[0]   # best suggestions (decoded to str)
                corrected.append(best)

    return corrected



if __name__ == '__main__':

    test = 'Белять'

    print (spellchecker.spell(test))
    print(json.dumps(spellchecker.suggest(test),  sort_keys=True, ensure_ascii=False))

    cor = correct_words([u'приивет'])
    print(json.dumps(cor,  sort_keys=True, ensure_ascii=False))
