import gensim

from Approaches import util

''' method for finding differences in documents with the TextRank keyword extraction
    text_one: First text
    text_two: Second text
    ratio_of_text: float that defines the number of extracted keywords as a percentage of all words in this text
    differentiation_method: number of the used approach, tow inputs are possible:
        simple: This approach corresponds to the simple differentiation that compares the n best keywords of the documents 
        and returns all words that are not equal with a word of the other document
        semantic: This approach corresponds to the semantic differentiation that compares the n best keywords of both texts 
        and removes all keywords that are in a synonym, hypernym or hyponym relationship. The remaining keywords are 
        returned.
'''


def textRank(text_one, text_two, ratio_of_text, differentiation_method):
    # --------------------------------------looking for wrong inputs------------------------------------------------
    if not type(text_one) == str or not type(text_two) == str:
        return ['the first or second document is not a text']

    if not type(ratio_of_text) == float:
        return ['ratio_of_text is not a float']

    if ratio_of_text <= 0.0:
        return ['please select a number grater than 0.0 for ratio_of_text']

    if ratio_of_text > 1.0:
        return ['pleas select a number less than 1.0 for ratio_of_text']

    # --------------------------------------------text preprocessing----------------------------------------------------

    # preprocess texts and join list back to string
    text_one = ' '.join(util.preprocess(text_one))
    text_two = ' '.join(util.preprocess(text_two))

    # -------------------------------------------extracting keywords----------------------------------------------------

    # extract keywords from text, the number of keywords depends on the ratio of the text length
    keyword_one = gensim.summarization.keywords(text_one, ratio=ratio_of_text).split()
    keyword_two = gensim.summarization.keywords(text_two, ratio=ratio_of_text).split()

    # -------------------------------------------extracting text differences--------------------------------------------

    # approach one
    if differentiation_method == 'simple':
        return util.simple_differentiation(keyword_one, keyword_two)

    # approach two
    elif differentiation_method == 'semantic':
        return util.semantic_differentiation(keyword_one, keyword_two)
