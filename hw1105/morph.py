from pymorphy2 import MorphAnalyzer
import random
morph = MorphAnalyzer()
import re

text = input('введите предложение: ')

twords = text.split(' ')

def words_from_file(filename):
    words = []
    with open (filename, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            word = line.split('\t')[1]
            word = word.rstrip('\n')
            words.append(word)
    return words

words = words_from_file('1grams-3.txt')

new_words = []
for tword in twords:
    new_grs = []
    ana_tword = morph.parse(tword)[0]
    word = random.choice(words)
    ana_random_word = morph.parse(word)[0]
    while ana_random_word.tag.POS != ana_tword.tag.POS:
        word = random.choice(words)
        ana_random_word = morph.parse(word)[0]
    else:
        ana_tag_to_grs = re.sub(' ', ',', str(ana_tword.tag)) 
        grs = ana_tag_to_grs.split(',')
        for gr in grs[1:]:
            try:
                ana_word = ana_random_word
                ana_word = ana_word.inflect({gr})
                if ana_word != None:
                    new_grs.append(gr)
            except AttributeError:
                pass
        for gr in new_grs:
            final_word = ana_random_word.inflect({gr})
    new_words.append(final_word.word)
    

new_sentence = ' '.join(new_words)
print(new_sentence)
    
    
    
    
