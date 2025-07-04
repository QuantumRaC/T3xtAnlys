import spacy
from spacy.lang.zh.examples import sentences
from spacy import displacy
from collections import Counter
from textblob import TextBlob
from analyze import text_analyze_eng #, text_analyze_chn

lang = 'Eng'

def main():
    if lang == 'Eng':
            nlp = spacy.load("en_core_web_md")
            # read input text
            with open("input/english_sample.txt", "r", encoding="utf-8") as f:
                input_text = f.read()
            text_analyze_eng(input_text)
    elif lang == 'Chn':
        nlp = spacy.load("zh_core_web_sm")
        # read input text
        with open("input/chinese_sample.txt", "r", encoding="utf-8") as f:
            input_text = f.read()
        # text_analyze_chn(input_text)
    

if __name__ == '__main__':
    main()
