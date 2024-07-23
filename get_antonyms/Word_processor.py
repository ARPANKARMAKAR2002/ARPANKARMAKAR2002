import nltk
from nltk.corpus import wordnet


def get_definitions(word):
    definitions = wordnet.synsets(word)
    return [syn.definition() for syn in definitions]

def get_synonyms(word):
    synonyms = []
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.append(lemma.name())
    return list(set(synonyms))

def get_antonyms(word):
    antonyms = []
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            if lemma.antonyms():
                antonyms.extend([ant.name() for ant in lemma.antonyms()])
    return list(set(antonyms))


