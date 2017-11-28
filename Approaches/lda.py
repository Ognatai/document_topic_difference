import re

import gensim

from Approaches import util

''' method for finding differences in documents with the LDA model
    text_one: First text
    text_two: Second text
    number_of_topics: number of topics that should be generated from the corpus, default number is 5
    Every time this method is called the LDA model is trained in the corpus because every time new documents could build
    a completely different corpus.
'''


def lda(text_one_original, text_two_original, number_of_topics):
    # --------------------------------------looking for wrong inputs------------------------------------------------
    if not type(text_one_original) == str or not type(text_two_original) == str:
        return ['the first or second document is not a text']

    if not type(number_of_topics) == int:
        return ['number_of_topics is not a integer']

    if number_of_topics < 1:
        return ['please select a number grater than 0 for number_of_topics']

    # --------------------------------------------text preprocessing----------------------------------------------------

    # preprocess texts
    text_one = util.preprocess(text_one_original)
    text_two = util.preprocess(text_two_original)

    # -----------------------------------------------extract topics-----------------------------------------------------

    # merge both texts to one corpus
    corpus = [text_one, text_two]

    # map every unique word to a id
    id2word = gensim.corpora.Dictionary(corpus)

    # turn into bag of words
    corpus = [id2word.doc2bow(text) for text in corpus]

    # train lda model with whole corpus
    lda = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=id2word, num_topics=number_of_topics, passes=10)

    # turn both texts to bag of words
    text_one = id2word.doc2bow(text_one)
    text_two = id2word.doc2bow(text_two)

    # compute the topics for the documents
    lda_one = lda[text_one]
    lda_two = lda[text_two]

    # -------------------------------------------extracting text differences--------------------------------------------
    same = False
    single_words = []
    result = []

    # convert the number tuple to the words of the topics
    topics_one = [lda.print_topic(topic[0]) for topic in lda_one]
    topics_two = [lda.print_topic(topic[0]) for topic in lda_two]

    # remove everything that do not start with a letter and tokenize, for better readability
    topics_one = [re.findall('[a-z]+[-,/]*', topic) for topic in topics_one]
    topics_two = [re.findall('[a-z]+[-,/]*', topic) for topic in topics_two]

    # preprocess again LDA gets  not preprocessed tokens while computing topics for the documents
    topics_one = [util.preprocess(' '.join(topic)) for topic in topics_one]
    topics_two = [util.preprocess(' '.join(topic)) for topic in topics_two]

    # remove all words from the topics in topics_one that are in topics_one and topics_two
    for topic in topics_one:
        for word in topic:
            for other_topic in topics_two:
                for other_word in other_topic:
                    if word == other_word:
                        same = True
            if not same:
                single_words.append(word)
            same = False
        if len(single_words) > 0:
            result.append(single_words)
        single_words = []

    return result
