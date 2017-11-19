#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import sys
import os.path
import json
import hunspell
sys.path.append("./lib")
# sys.path.append("/home/rustam/projects/panacea_ocr/lib/")

# spellchecker = hunspell.HunSpell('/usr/share/hunspell/en_US.dic', '/usr/share/hunspell/en_US.aff')
spellchecker = hunspell.HunSpell('/home/rustam/projects/panacea_ocr/lib/dict/Russian.dic',
'/home/rustam/projects/panacea_ocr/lib/dict/Russian.aff')
# spellchecker = hunspell.HunSpell('./lib/dict/med.blood.dic','./lib/dict/Russian.aff')
# spellchecker = hunspell.add_dic('./lib/dict/med.blood.dic')


def correct_words(words, add_to_dict=[]):
    """
    Автокоррекция из словаря на 1 вариант
    https://datascience.blog.wzb.eu/2016/07/13/autocorrecting-misspelled-words-in-python-using-hunspell/
    """

    # enc = spellchecker.get_dic_encoding()   # get the encoding for later use in decode()
    # print (enc)

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

def spell(words):
    """
    Проверка, есть ли в словаре заданное слово
    """

    correct = []
    for w in words:
        ok = spellchecker.spell(w)   # check spelling
        if ok:
            correct.append(w)

    return correct


def add(words):
    """
    Добавляем, новые фразы в наш кровавый словарь
    """

    print (words)
    for w in words:
        ok = spellchecker.spell(w)   # check spelling
        print (ok)
        print(json.dumps(spellchecker.stem(w),  sort_keys=True, ensure_ascii=False))
        if not ok:
            print ('add: ' + w)
            AppendWordsToDict([w])

    return


def AppendWordsToDict(WordList, Dict='./lib/dict/Russian.dic'):
    """
    Load the Hunspell dictionary and append the supplied words to it.
    """
    try:
        with open(os.path.join(Dict), 'a') as f:
            for word in WordList:
                f.write(word.encode('utf-8') + '\n')

        print '\nSUCCESS - {} words written '\
            'to the dictionary.\n'.format(len(WordList))

    except Exception as e:
        print e


if __name__ == '__main__':

    test = 'Белять'

    # print (spellchecker.spell(test))
    # print(json.dumps(spellchecker.suggest(test),  sort_keys=True, ensure_ascii=False))
    #
    # cor = correct_words([u'приивет'])
    # print(json.dumps(cor,  sort_keys=True, ensure_ascii=False

    if len(sys.argv) > 1:
        print sys.argv
        text = str(sys.argv[1])

    if text:
        add([text.decode('utf-8')])
