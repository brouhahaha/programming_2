
from pymorphy2 import MorphAnalyzer
import random
morph = MorphAnalyzer()
import re

text = input('введите предложение: ')

twords = text.split(' ')


def open_url (pageUrl):              #открывает страницу по заданному url
    import urllib.request  
    req = urllib.request.Request(pageUrl)
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('windows 1251')
    return html


def clean_tag (regex, obj_to_clean):         #очищает найденные строки от ненужного мусора, заданного рег.
    obj_to_add = re.sub (regex,'', obj_to_clean)
    return obj_to_add

def find_obj (html, regex):      # ищет по заданному регулярному выражению
    found = re.findall(regex, html)
    return found

def words():
    html = open_url('http://lib.ru/INOFANT/AZARO/skolian1.txt')
    clean = clean_tag('<.*?>.*?<.*?>', html)
    words = find_obj(clean, '[А-Яа-я]+')
    return words

words = words()
POS_list = []
words_to_inflect = {}

for word in words:
    ana = morph.parse(word)[0]
    POS = ana.tag.POS
    if POS_list.count(POS)== 0:
        POS_list.append(POS)
    
for item in POS_list:
    if item == 'NOUN':
        words_to_inflect['NOUN']={'femn':[], 'masc':[], 'neut':[]}
    else:
        words_to_inflect [item] = []

for word in words:
    ana = morph.parse(word)[0]
    POS = ana.tag.POS
    if POS == 'NOUN':
        try:
            words_to_inflect['NOUN'][str(ana.tag.gender)].append(word)
        except:
            KeyError
    else:
        words_to_inflect[POS].append(word)


new_words =[]   
for word in twords: 
    ana = morph.parse(word)[0]
    if str(ana.tag.POS) == 'NOUN':
       word1 = random.choice(words_to_inflect['NOUN'][ana.tag.gender])    
    else:
        word1 = random.choice(words_to_inflect[ana.tag.POS])
    new_word_ana = morph.parse(word1)[0]
    if ana.tag.POS == new_word_ana.tag.POS: 
        ana_tag_to_grs = re.sub(' ', ',', str(ana.tag)) 
        grs = ana_tag_to_grs.split(',')
    for gr in grs:
        if gr == 'Qual' or gr == 'inan' or gr == 'intr' or gr == 'impf' or gr == 'futr' or gr == 'pres':
            pass
        else:
            new_word_ana = new_word_ana.inflect({gr})
    new_words.append(new_word_ana.word)
print(' '.join(new_words))
