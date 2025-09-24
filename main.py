import spacy
from spacy.lang.zh.examples import sentences
from spacy import displacy
from collections import Counter
from textblob import TextBlob
from analyze import text_analyze_eng, text_analyze_chn

from langdetect import detect

from google import genai
import os

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)



def main():
    input_filename = 'borges_chinese_sample.txt'
    # connecting to Gemini
    with open("input/"+input_filename, "r", encoding="utf-8") as f:
        input_text = f.read()
    lang = detect(input_text)
    print(lang)
    if lang and lang == 'en':
        # nlp = spacy.load("en_core_web_md")
        prompt = text_analyze_eng(input_text)
    elif lang and lang == 'zh-cn':
       #  nlp = spacy.load("zh_core_web_sm")
        prompt = text_analyze_chn(input_text) + "\nThe text is a Chinese text and your audience are native Chinese speakers. Therefore, analyze it using Chinese."
    
    # print(prompt)
    
    response = client.models.generate_content(
    model="gemini-2.5-flash", contents=prompt)
    print(f"\n------------- \n{response.text}")

    

if __name__ == '__main__':
    main()
