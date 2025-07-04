import spacy
from spacy.lang.zh.examples import sentences
from spacy import displacy
from collections import Counter
import statistics
from textblob import TextBlob
from tabulate import tabulate

# helper function that outputs a dictionary of avg, s.d., range, & oscillation of the list.
def variance_measures(input_list):
    sd = statistics.stdev(input_list) if len(input_list) > 1 else 0
    avg = sum(input_list) / len(input_list) if len(input_list) > 0 else 0
    rnge = max(input_list) - min(input_list)
    if len(input_list) < 2:
        osc = 0
    else:
        osc = sum(1 for i in range(1, len(input_list)) if input_list[i] != input_list[i-1])
    osc = osc / (len(input_list) - 1) if len(input_list) > 1 else 0
    return {
        'average': avg,
        'stdev': sd,
        'range': rnge,
        'oscillation_ratio': osc
    }


def output_variance(variance_dict, measure_name):
    data = [
        ['Average均值', round(variance_dict['average'], 3)],
        ['S.d.标准差', round(variance_dict['stdev'], 3)],
        ['Range范围', variance_dict['range']],
        ['Osc % 波动', f"{variance_dict['oscillation_ratio'] * 100:.1f}%"]
    ]
    print(measure_name)
    print(tabulate(data, tablefmt="grd") + '\n')

def text_analyze_eng(input_text):
    nlp = spacy.load("en_core_web_md")
    tokens = [] # list of tokens (not excluding PUNCT)
    lemmas = [] # list of lemmas of ADJ, ADV, INTJ, NOUN, SCONJ, VERB or PROPN
    sent_lengths = [] # list of each sentence's length (not excluding PUNCT)
    token_lengths = [] # list of each token's (exclude PUNCT) length
    morphs = [] # a list of lists; each sublist is a sentence; each item is a token's morphs

    doc = nlp(input_text)
    print("Pipeline:", nlp.pipe_names)

    for sent in doc.sents:
        # parse into sentences (sent)
        sent_lengths.append(len(sent))
        # print(f"\nSentence: {sent.text}")
        morphs.append([])
        for token in sent:
            # Convert morph to string first
            morph_str = str(token.morph)
            morph_list = morph_str.split('|') if morph_str else []
            if len(morph_list) != 0: morphs[-1].append(morph_list) 
            tokens.append(token)
            if token.pos_ != 'PUNCT':
                token_lengths.append(len(token))
            if token.pos_ in ('ADJ', 'ADV', 'INTJ', 'NOUN', 'SCONJ', 'VERB', 'PROPN'):
                lemmas.append(token.lemma_)

    # displacy.serve(doc, style="dep", compact=True)
    # Extract all part-of-speech tags from tokens list
    pos_list = [token.pos_ for token in tokens] # part of speech
    dep_list = [token.dep_ for token in tokens] # dependency
    verb_tense_list = [token.tag_ for token in tokens if token.tag_.startswith('V')] # verb tenses
    pos_freq_tbl = Counter(pos_list) #frequency table of pos
    dep_freq_tbl = Counter(dep_list) #frequency table of dependency
    verb_tense_freq_tbl = Counter(verb_tense_list)
    lemma_freq_tbl = Counter(lemmas) #frequency table of lemmas for commonly seen words

    # print(morphs[:2])
    # print(tokens)

    sent_length_variance = variance_measures(sent_lengths)
    token_length_variance = variance_measures(token_lengths)

    print(f"Part of Speech: {pos_freq_tbl}\n")
    print(f"Dependency: {dep_freq_tbl}\n")
    print(f"Verb Tenses: {verb_tense_freq_tbl}\n")
    
    print(f"Repetition / Motifs: {lemma_freq_tbl}\n")
    print(sent_lengths)
    output_variance(sent_length_variance, 'Sentence Length (words)')
    print(token_lengths)
    output_variance(token_length_variance, "Token Length (char)(excluding PUNCT)")
    

    # Counting clauses per sentence
    clause_deps = ['ccomp', 'xcomp', 'advcl', 'relcl', 'conj']
    clauses_per_sent = []
    for sent in doc.sents:
        clause_count = sum(1 for token in sent if token.dep_ in clause_deps) + 1 # +1 for the main clause; total clauses per sentence
        clauses_per_sent.append(clause_count)
    
    clause_freq_variance = variance_measures(clauses_per_sent)
    print(clauses_per_sent)
    output_variance(clause_freq_variance, "Clauses per sentence")

    # assembling prompt
    with open("prompt_template.txt", "r", encoding="utf-8") as file:
        prompt_template = file.read()
    final_prompt = prompt_template.format(
        text_excerpt=input_text[:500],  # limit to first 500 characters or so
        avg_sentence_length=round(sent_length_variance['average'], 2),
        std_sentence_length=round(sent_length_variance['stdev'], 2),
        range_sentence_length=sent_length_variance['range'],
        osc_sentence_length=sent_length_variance['oscillation_ratio'],

        avg_token_length=round(token_length_variance['average'], 2),
        std_token_length=round(token_length_variance['stdev'], 2),
        range_token_length=token_length_variance['range'],
        osc_token_length=token_length_variance['oscillation_ratio'],

        avg_clauses_per_sentence=round(clause_freq_variance['average'], 2),
        std_clauses_per_sentence=round(clause_freq_variance['stdev'], 2),
        range_clauses_per_sentence=clause_freq_variance['range'],
        osc_clauses_per_sentence=clause_freq_variance['oscillation_ratio'],

        pos_freq=dict(pos_freq_tbl),
        dep_freq=dict(dep_freq_tbl),
        verb_tense_freq=dict(verb_tense_freq_tbl),
        lemma_freq=lemma_freq_tbl.most_common(5),
        morphs_sample=morphs[:2]
    )
    return final_prompt


def text_analyze_chn(input_text):
    # nlp = spacy.load("en_core_web_md")
    nlp = spacy.load("zh_core_web_sm")
    tokens = [] # list of tokens (not excluding PUNCT)
    lemmas = [] # list of lemmas of ADJ, ADV, INTJ, NOUN, SCONJ, VERB or PROPN
    sent_lengths = [] # list of each sentence's length (not excluding PUNCT)
    token_lengths = [] # list of each token's (exclude PUNCT) length
    morphs = [] # a list of lists; each sublist is a sentence; each item is a token's morphs

    doc = nlp(input_text)
    print("Pipeline:", nlp.pipe_names)

    for sent in doc.sents:
        # parse into sentences (sent)
        sent_lengths.append(len(sent))
        # print(f"\nSentence: {sent.text}")
        morphs.append([])
        for token in sent:
            # Convert morph to string first
            morph_str = str(token.morph)
            morph_list = morph_str.split('|') if morph_str else []
            if len(morph_list) != 0: morphs[-1].append(morph_list) 
            tokens.append(token)
            if token.pos_ != 'PUNCT':
                token_lengths.append(len(token))
            if token.pos_ in ('ADJ', 'ADV', 'INTJ', 'NOUN', 'SCONJ', 'VERB', 'PROPN'):
                lemmas.append(token.lemma_)

    # displacy.serve(doc, style="dep", compact=True)
    # Extract all part-of-speech tags from tokens list
    pos_list = [token.pos_ for token in tokens] # part of speech
    dep_list = [token.dep_ for token in tokens] # dependency
    verb_tense_list = [token.tag_ for token in tokens if token.tag_.startswith('V')] # verb tenses
    pos_freq_tbl = Counter(pos_list) #frequency table of pos
    dep_freq_tbl = Counter(dep_list) #frequency table of dependency
    verb_tense_freq_tbl = Counter(verb_tense_list)
    lemma_freq_tbl = Counter(lemmas) #frequency table of lemmas for commonly seen words

    # print(morphs[:2])
    # print(tokens)

    sent_length_variance = variance_measures(sent_lengths)
    token_length_variance = variance_measures(token_lengths)

    print(f"Part of Speech: {pos_freq_tbl}\n")
    print(f"Dependency: {dep_freq_tbl}\n")
    print(f"Verb Tenses: {verb_tense_freq_tbl}\n")
    
    print(f"Repetition / Motifs: {lemma_freq_tbl}\n")
    print(sent_lengths)
    output_variance(sent_length_variance, 'Sentence Length (words)')
    print(token_lengths)
    output_variance(token_length_variance, "Token Length (char)(excluding PUNCT)")
    

    # Counting clauses per sentence
    clause_deps = ['ccomp', 'xcomp', 'advcl', 'relcl', 'conj']
    clauses_per_sent = []
    for sent in doc.sents:
        clause_count = sum(1 for token in sent if token.dep_ in clause_deps) + 1 # +1 for the main clause; total clauses per sentence
        clauses_per_sent.append(clause_count)
    
    clause_freq_variance = variance_measures(clauses_per_sent)
    print(clauses_per_sent)
    output_variance(clause_freq_variance, "Clauses per sentence")

    # assembling prompt
    with open("prompt_template_Chn.txt", "r", encoding="utf-8") as file:
        prompt_template = file.read()
    final_prompt = prompt_template.format(
        text_excerpt=input_text[:500],  # limit to first 500 characters or so
        avg_sentence_length=round(sent_length_variance['average'], 2),
        std_sentence_length=round(sent_length_variance['stdev'], 2),
        range_sentence_length=sent_length_variance['range'],
        osc_sentence_length=sent_length_variance['oscillation_ratio'],

        avg_token_length=round(token_length_variance['average'], 2),
        std_token_length=round(token_length_variance['stdev'], 2),
        range_token_length=token_length_variance['range'],
        osc_token_length=token_length_variance['oscillation_ratio'],

        avg_clauses_per_sentence=round(clause_freq_variance['average'], 2),
        std_clauses_per_sentence=round(clause_freq_variance['stdev'], 2),
        range_clauses_per_sentence=clause_freq_variance['range'],
        osc_clauses_per_sentence=clause_freq_variance['oscillation_ratio'],

        pos_freq=dict(pos_freq_tbl),
        dep_freq=dict(dep_freq_tbl),
        verb_tense_freq=dict(verb_tense_freq_tbl),
        lemma_freq=lemma_freq_tbl.most_common(5),
        morphs_sample=morphs[:2]
    )
    return final_prompt
