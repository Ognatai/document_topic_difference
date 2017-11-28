from heapq import nlargest
from operator import itemgetter
from collections import Counter

from gensim import corpora
from gensim import models

from Approaches import util

''' method for finding differences in documents with the tf-idf computation
    text_one: First text
    text_two: Second text
    ratio_of_best_words: Float that defines the n percent words, per document, with the highest tf-idf value that 
        should be considered for the differences between the documents, n depends on the unique tokens in the text
    differentiation_method: number of the used approach, tow inputs are possible:
        simple: This approach corresponds to the simple differentiation that compares the n best words of the documents and
         returns all words that are not equal with a word of the other document
        semantic: This approach corresponds to the semantic differentiation that compares the n best words of both texts and 
        removes all words that are in a synonym, hypernym or hyponym relationship. The remaining words are returned.
'''


def tfidf(text_one, text_two, ratio_of_best_words, differentiation_method):
    # --------------------------------------looking for wrong inputs------------------------------------------------
    if not type(text_one) == str or not type(text_two) == str:
        return ['the first or second document is not a text']

    if not type(ratio_of_best_words) == float:
        return ['number_of_best_words is not a float']

    if ratio_of_best_words <= 0.0:
        return ['please select a number grater than 0.0 for number_of_best_words']

    if ratio_of_best_words > 1.0:
        return ['pleas select a number less than 1.0 for number_of_best_words']

    # ----------------------------------------------text preprocessing----------------------------------------------

    # preprocess texts
    text_one = util.preprocess(text_one)
    text_two = util.preprocess(text_two)

    # check if number of words to compare is less than the number of words in the smallest text
    if ratio_of_best_words > min(len(text_one), len(text_two)):
        message = 'chosen number is bigger than tokens in texts please choose a number < ' + str(min(len(text_one),
                                                                                                     len(text_two)))
        return [message]

    # -------------------------------------extracting most important text concepts--------------------------------------

    # compute number_of_best_words for both texts and convert to integer, only whole words can be retrieved
    number_of_best_words1 = int(round(len(Counter(text_one)) * ratio_of_best_words))
    number_of_best_words2 = int(round(len(Counter(text_two)) * ratio_of_best_words))

    # merge both texts to one corpus
    corpus = [text_one, text_two]

    # map every unique word to a id
    dictionary = corpora.Dictionary(corpus)

    # count the occurrence of every unique word and map the occurrence to the word id
    # convert the corpus to a bag of words
    corpus = [dictionary.doc2bow(text) for text in corpus]

    # train the transformation model on the corpus, from now on tfidf is a read-only object
    tfidf = models.TfidfModel(corpus)

    # apply tf-idf to whole corpus
    corpus_tfidf = tfidf[corpus]

    # split corpus back in documents
    tfidf_one = corpus_tfidf[0]
    tfidf_two = corpus_tfidf[1]

    # make dictionary to an actual dictionary and switch key and value
    dictionary = dictionary.token2id
    dictionary = {y: x for x, y in dictionary.items()}

    # map ids back to words
    tfidf_one = [(dictionary[word], tfidf) for (word, tfidf) in tfidf_one]
    tfidf_two = [(dictionary[word], tfidf) for (word, tfidf) in tfidf_two]

    # get the defined number word with the biggest tf-idf
    # the tf-idf value is on position 1
    one_largest = nlargest(number_of_best_words1, tfidf_one, key=itemgetter(1))
    two_largest = nlargest(number_of_best_words2, tfidf_two, key=itemgetter(1))

    # drop the tf-idf value
    one_largest = [word for (word, tfidf) in one_largest]
    two_largest = [word for (word, tfidf) in two_largest]

    # -------------------------------------------extracting text differences--------------------------------------------

    # approach one
    if differentiation_method == 'simple':
        return util.simple_differentiation(one_largest, two_largest)

    # approach two
    elif differentiation_method == 'semantic':
        return util.semantic_differentiation(one_largest, two_largest)
