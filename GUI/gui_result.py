import tkinter

from Approaches import lda
from Approaches import textRank
from Approaches import tf_idf

import os


# method for computing the result
def computing_result(text1, text2, num_entry, approach, differentiation_method):
    if approach == 'LDA':
        result = lda.lda(text1, text2, num_entry)
        gui(text1, text2, result, approach, differentiation_method)

    elif approach == 'TextRank':
        result = textRank.textRank(text1, text2, num_entry, differentiation_method)
        gui(text1, text2, result, approach, differentiation_method)

    else:
        result = tf_idf.tfidf(text1, text2, num_entry, differentiation_method)
        gui(text1, text2, result, approach, differentiation_method)


# method to display the result in a new window
def gui(text1, text2, result, approach, differentiation_method):
    top = tkinter.Toplevel()
    show_result = ''

    show_minor = ''
    if approach != 'LDA':
        if differentiation_method == 'simple':
            show_minor = 'differentiation method: simple differentiation'
        else:
            show_minor = 'differentiation method: semantic differentiation'

    approach_txt = 'Words/topics that differentiate the left text from the right one. \n Computed with:  ' \
                   + approach + '\n' + show_minor
    title_text = approach + ' ' + show_minor

    top.title(title_text)

    # show all words of a topic in one line
    if approach == 'LDA':
        tmp = 0

        for list1 in result:
            tmp += 1
            topic = ', '.join(list1)
            show_result = show_result + 'topic ' + str(tmp) + ': ' + topic + '\n'

    # if approach is not LDA show all words beneath one another
    else:
        show_result = '\n'.join(result)

    # text on in the upper left
    scrollbar1 = tkinter.Scrollbar(top)
    scrollbar1h = tkinter.Scrollbar(top, orient=tkinter.HORIZONTAL)
    text_out1 = tkinter.Text(top, yscrollcommand=scrollbar1.set, xscrollcommand=scrollbar1h.set, height=20)
    text_out1.insert(tkinter.INSERT, text1)
    text_out1.grid(row=0)
    scrollbar1.grid(row=0, column=1, sticky=tkinter.N + tkinter.S)
    scrollbar1.config(command=text_out1.yview)
    scrollbar1h.grid(row=1, sticky=tkinter.E + tkinter.W)
    scrollbar1h.config(command=text_out1.xview)

    # text two in the upper right
    scrollbar2 = tkinter.Scrollbar(top)
    scrollbar2h = tkinter.Scrollbar(top, orient=tkinter.HORIZONTAL)
    text_out2 = tkinter.Text(top, yscrollcommand=scrollbar2.set, xscrollcommand=scrollbar2h.set, height=20)
    text_out2.insert(tkinter.INSERT, text2)
    text_out2.grid(row=0, column=2)
    scrollbar2.grid(row=0, column=3, sticky=tkinter.N + tkinter.S)
    scrollbar2.config(command=text_out2.yview)
    scrollbar2h.grid(row=1, sticky=tkinter.E + tkinter.W, column=2)
    scrollbar2h.config(command=text_out2.xview)

    # approach name
    tkinter.Label(top, text=approach_txt).grid(row=2, columnspan=3)

    # result of text one in the lower left
    scrollbar3 = tkinter.Scrollbar(top)
    result_out1 = tkinter.Text(top, yscrollcommand=scrollbar3.set, height=15)
    result_out1.insert(tkinter.INSERT, show_result)
    result_out1.grid(row=3, columnspan=3)
    scrollbar3.grid(row=3, column=3, sticky=tkinter.N + tkinter.S + tkinter.W)
    scrollbar3.config(command=result_out1.yview)

    # close button
    close = tkinter.Button(top, text='close', command=top.destroy)
    close.grid(row=5, column=2, sticky=tkinter.N + tkinter.E)
