# -*- coding: utf-8 -*-
"""Arabert mehdi.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1alj5zRLHtqq9F7i0wqfkmUenLmVVg_wr
"""

!pip install transformers
!pip install transformers
!pip install farasapy
!pip install pyarabic
!pip install preprocess
!pip install arabert
!git clone github.com/aub-mind/arabert
from transformers import pipeline
from arabert.preprocess import ArabertPreprocessor
MODEL_NAME = 'aubmindlab/bert-base-arabertv02-twitter'

fill_mask = pipeline(task="fill-mask",model=MODEL_NAME,tokenizer=MODEL_NAME)
print(fill_mask(" الحياة بسيطة حقا ، لكننا نصر على جعلها [MASK] " ))

def Substitution(word, word2):  # return true if exists one and only onesubstituion error
    if len(word) == len(word2):
        l = []
        for i in range(len(word)):
            if word[i] == word2[i]:
                l.append(0)
            else:
                l.append(1)
        return (sum(l) == 1)
    else:
        return(False)
def Inversion(word, word2):
    if len(word) == len(word2):  # returns true if exists one and only inversion error
        l1 = []
        l2 = []
        for i in range(len(word)):
            if word[i] == word2[i]:
                l1.append(0)
            else:
                l1.append(1)
                l2.append(word[i])
                l2.append(word2[i])
        if sum(l1) == 2:
            return(l2[0] == l2[3] and l2[1] == l2[2])
        else:
            return(False)
    else:
        return(False)

def Ajoutsup(word1, word2):  # ajout/suppression d'un seul caracter
    w1 = set(word1)
    w2 = set(word2)
    maxi = max(len(w1-w2), len(w2-w1))
    if maxi != 1:
        return(False)
    else:
        if len(w1)-len(w2) == 1:
            lw1 = list(word1)
            lw1.remove(''.join(w1-w2))
            s = ''.join(str(x) for x in lw1)
            return(s == word2)
        elif len(w1)-len(w2) == -1:
            lw2 = list(word2)
            lw2.remove(''.join(w2-w1))
            s = ''.join(str(x) for x in lw2)
            return(s == word1)
        else:
            return(False)





def similaire(words, corpustoken):
    for word in words:
        for c in corpustoken:
            if Ajoutsup(word, c):
                return(word)
            elif Inversion(word, c) or Substitution(word, c):  # inversion / substitution
                return(word)
    return('')

def replace(mask, text):
    text = text.split()
    text = list(map(lambda x: x.replace(mask, '[MASK]'), text))
    text = ' '.join(str(x) for x in text)
    return(text)

import re
import nltk
nltk.download('punkt')
nltk.download("stopwords")
arb_stopwords = set(nltk.corpus.stopwords.words("arabic"))

def clean_str(text):
    search = ["أ","إ","آ","ة","_","-","/",".","،"," و "," يا ",'"',"ـ","'","ى","\\",'\n', '\t','&quot;','?','؟','!']
    replace = ["ا","ا","ا","ه"," "," ","","",""," و"," يا","","","","ي","",' ', ' ',' ',' ? ',' ؟ ',' ! ']

    #remove tashkeel
    p_tashkeel = re.compile(r'[\u0617-\u061A\u064B-\u0652]')
    text = re.sub(p_tashkeel,"", text)

    #remove longation
    p_longation = re.compile(r'(.)\1+')
    subst = r"\1\1"
    text = re.sub(p_longation, subst, text)

    text = text.replace('وو', 'و')
    text = text.replace('يي', 'ي')
    text = text.replace('اا', 'ا')

    for i in range(0, len(search)):
        text = text.replace(search[i], replace[i])

    text = " ".join([w for w in text.split(" ") if not w in arb_stopwords])

    text = text.strip()

    return text

def analyse(text):
    ok =True
    res=[]
    print("\n","La phrase = ",text,"\n")
    for mask in text.split():
        masked_text = replace(mask,text)
        words = fill_mask(masked_text)
        s=[]
        t=[]
        for e in words:
    #        t.append(e['token_str'])
            t.append(clean_str(e['token_str']))
            s.append(e['sequence'])
        correct = similaire(t, [clean_str(mask)]) #les mots parmi les mots générs qui ressemblent au mot à analyser
        if correct != mask and correct:
            print("Erreur : ", mask )
            #print("Erreur : ", mask , " || correction : ",correct,"")
            ok = False
            res.append((mask,correct))
    if ok :
        print("Cette phrase contient 0 erreurs ")
    return(res)

Text1 = ['الحياة بسيطة حقا ، لكننا نصر على جعلها معدة'
,'ارجع البعض السبب إلي ارتفاع اسفار النفط'
,'تعد البطالة احد اهم الظواهر التى تلازم المستمع'
,'لو أعطيت الأحمق خنجرا أصبت قاتلا'
,'لمسة واحدة للضفدع الذهبي السام تسبب الوفاة']

for i in range(0,len(Text1)):
    '/n'
    analyse(Text1[i])
    '/n'

# Reading DataSet
import pandas as pd
df = pd.read_csv('arabic.txt',sep="\n")
df.columns = ['text']
df

df['Label'] = df['text'].apply(lambda x: x.split("|")[0] )
df['text'] = df['text'].apply(lambda x: x.split("|")[1] )
df
