import spacy
from spacy.lang.zh.examples import sentences
from spacy import displacy
from collections import Counter
from textblob import TextBlob
from analyze import text_analyze_eng, text_analyze_chn

from google import genai

lang = 'Chn'

def main():

    # connecting to Gemini
    client = genai.Client()
    
    if lang == 'Eng':
            nlp = spacy.load("en_core_web_md")
            # read input text
            with open("input/english_sample.txt", "r", encoding="utf-8") as f:
                input_text = f.read()
            prompt = text_analyze_eng(input_text)
    elif lang == 'Chn':
        nlp = spacy.load("zh_core_web_sm")
        # read input text
        with open("input/chinese_sample.txt", "r", encoding="utf-8") as f:
            input_text = f.read()
        prompt = text_analyze_chn(input_text)

    # print(prompt)
    
    response = client.models.generate_content(
    model="gemini-2.5-flash", contents=prompt)
    print(f"\n ------------- \n{response.text}")

    

if __name__ == '__main__':
    main()
