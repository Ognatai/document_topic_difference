from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import nltk


# --------------------------------------------------Preprocessing-------------------------------------------------------

def preprocess(text):
    # convert to lowercase, tokenize text, remove everything that's not a word
    text = text.lower()
    text = nltk.word_tokenize(text)
    text = [word for word in text if any(letter.isalpha() for letter in word)]

    # tag words with part of speech tags
    text = nltk.pos_tag(text)

    # change tags to wordnet tags
    text = [(word, get_wordnet_pos(pos)) for (word, pos) in text]

    # remove stopwords
    wo_stop = [(word, pos) for (word, pos) in text if word not in stopwords.words('english')]

    # remove all untagged words
    wo_stop = [(word, pos) for (word, pos) in wo_stop if pos != '']

    # remove every token < 3 characters
    wo_stop = [(word, pos) for (word, pos) in wo_stop if len(word) > 2]

    # lemmatize the text with word net
    wordnet_lemmatizer = WordNetLemmatizer()
    lemma = [wordnet_lemmatizer.lemmatize(word, pos=pos) for (word, pos) in wo_stop]

    return lemma


# ---------------------------------------change nltk POS Tags to Wordnet tags-------------------------------------------

def get_wordnet_pos(pos_tag):
    noun = ['CD', 'FW', 'NN', 'NNS', 'NNP', 'NNPS']
    adjective = ['JJ', 'JJR', 'JJS']
    adverb = ['PDT', 'IN', 'DT', 'MD', 'RB', 'RBR', 'RBS', 'RP']
    verb = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']

    if pos_tag in noun:
        return 'n'

    elif pos_tag in adjective:
        return 'a'

    elif pos_tag in adverb:
        return 'r'

    elif pos_tag in verb:
        return 'v'

    else:
        return ''


# --------------------------------------check if word is synonym of another---------------------------------------------

def check_wordnet_synonym(word_one, word_two):
    word_synonyms = []

    # find all synonyms for word one
    for synset in wordnet.synsets(word_one):

        # don't write the word itself in the list
        for lemma in synset.lemma_names():
            if lemma != word_one:
                word_synonyms.append(lemma)

    # check if second word is in the synonym list of the first one
    if word_two in word_synonyms:
        return True
    else:
        return False


# --------------------------------------check if word is a hypernym of another------------------------------------------

def check_wordnet_hypernym(word_one, word_two):
    word_hypernyms = []

    if len(wordnet.synsets(word_one)) > 0:

        # find all hypernyms of the first word
        for words in wordnet.synsets(word_one)[0].hypernyms():

            # don't write the word itself in the list
            for lemma in words.lemma_names():
                if lemma != word_one:
                    word_hypernyms.append(lemma)

        # check if second word is in the hypernym list of the first one
        if word_two in word_hypernyms:
            return True
        else:
            return False

    else:
        return False


# --------------------------------------check if word is a hyponym of another-------------------------------------------

def check_wordnet_hyponym(word_one, word_two):
    word_hyponyms = []

    if len(wordnet.synsets(word_one)) > 0:

        # find all hyponyms of the first word
        for words in wordnet.synsets(word_one)[0].hyponyms():

            # don't write the word itself in the list
            for lemma in words.lemma_names():
                if lemma != word_one:
                    word_hyponyms.append(lemma)

        # check if second word is in the hyponym list of the first one
        if word_two in word_hyponyms:
            return True
        else:
            return False

    else:
        return False


# ----------------------------approach one: check if words of one list are in other list--------------------------------

def simple_differentiation(list_one, list_two):
    # remove words that are in both lists
    result = [word for word in list_one if word not in list_two]

    # return the differences
    return result


# ---------approach two: check if words of one list are synonym, hypernom or hyponym of words in other list-------------

def semantic_differentiation(list_one, list_two):
    result = []
    same = False

    # remove all words that are synonyms, hypernyms or hyponyms to one another
    for word in list_one:
        for word2 in list_two:
            if check_wordnet_synonym(word, word2) or check_wordnet_hypernym(word, word2) \
                    or check_wordnet_hyponym(word, word2):
                same = True
        if not same:
            result.append(word)
        same = False

    # return the differences
    return result
