
from farasa.stemmer import FarasaStemmer

import pandas as pd
import numpy as np
import re
import string
import argparse
import json
import os

stop_word_path = "stop.txt"


class ArCleanText:
    def __init__(self):
        
        self.arabic_punctuations = '''`\r÷×؛<>_()*&^%][ـ،/:"؟.,'{}~¦+|!”…“–ـ21\n'''
        self.english_punctuations = string.punctuation
        self.punctuations_list = self.arabic_punctuations + self.english_punctuations
        self.arabic_diacritics = re.compile("""
                                             ّ    | # Tashdid
                                             َ    | # Fatha
                                             ً    | # Tanwin Fath
                                             ُ    | # Damma
                                             ٌ    | # Tanwin Damm
                                             ِ    | # Kasra
                                             ٍ    | # Tanwin Kasr
                                             ْ    | # Sukun
                                            ـ     # Tatwil/Kashida""", re.VERBOSE)

        self.arabic_stop_words = pd.read_csv(stop_word_path, header=None)
        self.arabic_stop_words = self.arabic_stop_words[0].unique().tolist()
        self.farasa_stemmer = FarasaStemmer(interactive=True)
        
        
    def normalize_arabic(self,text):
        text = re.sub("[إأآا]", "ا", text)
        text = re.sub("ى", "ي", text)
        text = re.sub("ؤ", "ء", text)
        text = re.sub("ئ", "ء", text)
        text = re.sub("ة", "ه", text)
        text = re.sub("گ", "ك", text)
        return text 
    
    def remove_diacritics(self,text):
        text = str(text)
        text = re.sub(self.arabic_diacritics, '', text)
        return text
    
    def remove_arabic_punctuations(self,text):
        translator = str.maketrans('', '', self.punctuations_list)
        return text.translate(translator)
    
    def remove_arabic_repeating_char(self,text):
        return re.sub(r'(.)\1+', r'\1', text)
  
    def remove_english_character(self,text):
        text=re.sub(r"[a-zA-z]+","", text)
        text=re.sub(r"$\d+\W+|\b\d+\b|\W+\d+$", "", text)
        return text 
    
    def ar_emoji_extractor(self,text):
      try:
        for key, value in self.emojis_data.items():
          for ch in text:
            if key in ch:
              text = re.sub(ch,value,text)
        return str(text)
      except:
        return text
    
    def arabic_preprocessing(self,x):
        
      x=self.remove_diacritics(x)
      #x=self.remove_arabic_repeating_char(x)
      x=self.normalize_arabic(x)
      x= ' '.join(word for word in x.split() if word[0]!='#')
      x=self.remove_arabic_punctuations(x)
      x = x.replace('#','')
      x = [i for i in x.split() if i not in self.arabic_stop_words]
      x = " ".join(x)
      x = re.sub((r"^[\W]*"), "", x)
      x = re.sub((r"\s[\W]\s"), ", ", x)
#       x = [i for i in x.split() if len(i)>1]
#       x = " ".join(x)
      x=  [i for i in x.split() if len(i)<16]
      x=" ".join(x)
      x=self.remove_english_character(x)
      x= self.farasa_stemmer.stem(x) 
      x = ''.join(x.splitlines())
      return x 


        
