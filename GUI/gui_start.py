import tkinter
from tkinter import filedialog
import os

from GUI import gui_result

# bunch of variables
root = tkinter.Tk()
path_one = tkinter.StringVar(None)
path_two = tkinter.StringVar(None)
default_option = tkinter.StringVar(None)
number_approach = tkinter.IntVar()
number_lable = tkinter.Label(root, text='')
approach_lable = tkinter.Label(root, text='')
radio_one = tkinter.Radiobutton(root, text="simple differentiation", variable=number_approach, value=1)
radio_two = tkinter.Radiobutton(root, text="semantic differentiation", variable=number_approach, value=2)
num_entry = tkinter.Entry(root)

path_one.set('')
path_two.set('')
text1 = ''
text2 = ''

# method for choosing a file
def open_it_1():
    global text1
    file = filedialog.askopenfilename(parent=root, title='Choose a file')
    path_one.set(file)
    if os.path.exists(file):
        with open(file) as f:
            text1 = f.read()
    else:
        text1 = 'Path for text one or two not valid!'

# method for choosing a second file
def open_it_2():
    global text2
    file = filedialog.askopenfilename(parent=root, title='Choose a file')
    path_two.set(file)
    if os.path.exists(file):
        with open(file) as f:
            text2 = f.read()
    else:
        text2 = 'Path for text one or two not valid!'

# on change dropdown value, display field depending on the chosen approach
def change_dropdown(*args):
    if default_option.get() == 'LDA':
        # lable for topic number
        number_lable.config(text='Provide a number of topics')
        number_lable.grid(row=3, sticky=tkinter.W)
        # entry for topic number
        num_entry.delete(0, tkinter.END)
        num_entry.insert(0, '5')
        num_entry.grid(row=3, column=1, sticky=tkinter.W)
        # clear the approach lable and radiobuttons
        approach_lable.grid_remove()
        radio_one.grid_remove()
        radio_two.grid_remove()
        # compute button
        compute_button.grid(row=5, column=1)

    elif default_option.get() == 'TextRank':
        # lable for text ratio
        number_lable.config(text='Provide a text ratio')
        number_lable.grid(row=3, sticky=tkinter.W)
        # entry for text ratio
        num_entry.delete(0, tkinter.END)
        num_entry.insert(0, '0.33')
        num_entry.grid(row=3, column=1, sticky=tkinter.W)
        # lable for approach
        approach_lable.config(text='Choose a differentiation method')
        approach_lable.grid(row=4, sticky=tkinter.W)
        # radiobutton simple differentiation
        radio_one.grid(row=4, column=1)
        radio_one.select()
        # radiobutton semantic differentiation
        radio_two.grid(row=4, column=2)
        # compute button
        compute_button.grid(row=5, column=1)

    elif default_option.get() == 'tf-idf':
        # lable for number of best words
        number_lable.config(text='Provide a ratio of best words')
        number_lable.grid(row=3, sticky=tkinter.W)
        # entry for best words
        num_entry.delete(0, tkinter.END)
        num_entry.insert(0, '0.33')
        num_entry.grid(row=3, column=1, sticky=tkinter.W)
        # lable for approach
        approach_lable.config(text='Choose a differentiation method')
        approach_lable.grid(row=4, sticky=tkinter.W)
        # radiobutton simple differentiation
        radio_one.grid(row=4, column=1)
        radio_one.select()
        # radiobutton semantic differentiation
        radio_two.grid(row=4, column=2)
        # compute button
        compute_button.grid(row=5, column=1)

# link function to change drop-down
default_option.trace('w', change_dropdown)


# function to actually compute the whole thing
def compute():
    path_one = path1.get()
    path_two = path2.get()
    if default_option.get() == 'LDA':
        if num_entry.get().isdigit():
            topic_num = int(num_entry.get())
        else:
            topic_num = num_entry.get()
        gui_result.computing_result(text1, text2, topic_num, 'LDA', '')

    elif default_option.get() == 'TextRank':
        if num_entry.get().isdigit() or '.' in num_entry.get():
            text_ratio = float(num_entry.get())
        else:
            text_ratio = num_entry.get()
        if number_approach.get() == 1:
            differentiation_method = 'simple'
        else:
            differentiation_method = 'semantic'
        gui_result.computing_result(text1, text2, text_ratio, 'TextRank', differentiation_method)

    else:
        if num_entry.get().isdigit() or '.' in num_entry.get():
            best_words = float(num_entry.get())
        else:
            best_words = num_entry.get()
        if number_approach.get() == 1:
            differentiation_method = 'simple'
        else:
            differentiation_method = 'semantic'
        gui_result.computing_result(text1, text2, best_words, 'tf-idf', differentiation_method)


# window title
root.title('Comparison of approaches for detecting topical differences of text documents')

# variable declaration could not be made above, function is needed before
compute_button = tkinter.Button(text='compute', command=compute)

# buttons to click for file choosing
tkinter.Button(text="Text One", command=open_it_1).grid(row=0, column=4)
tkinter.Button(text="Text Two", command=open_it_2).grid(row=1, column=4)

# text fields where the chosen path will be displayed
path1 = tkinter.Entry(root, textvariable=path_one, width=100)
path2 = tkinter.Entry(root, textvariable=path_two, width=100)

# placing the text fields in the GUI
path1.grid(row=0, columnspan=4)
path2.grid(row=1, columnspan=4)

# Dictionary with options for drop down
approaches = {'LDA', 'TextRank', 'tf-idf'}

# set the default option
default_option.set('Choose a approach')

# drop-down to choose a approach
drop_down = tkinter.OptionMenu(root, default_option, *approaches)
tkinter.Label(root, text="Choose a approach").grid(row=2, sticky=tkinter.W)
drop_down.grid(row=2, column=1)

# close button
tkinter.Button(text='close', command=root.destroy).grid(row=5, column=4)

root.mainloop()
