# To install the NLTK Python Library:  pip install --user -U nltk 
from nltk.tokenize import word_tokenize
import re
import unicodedata

def preprocess_question(question):
    """
    This method does the preprocessing of Questions 
    from the Database
    param: Question - The Question object to be preprocessed
    return: returns the Question Object
    """
    question = preprocess_title(question)
    return question

def preprocess_title(title):
    """
    This method makes the text lower, removes white space and rebuilds the 
    titles text
    """
    temp = title.lower()
    temp= remove_double_space(temp.replace('\n', ' '))
    temp = tokenize_and_rebuild(temp)
    return temp

def remove_double_space(test):
    while '  ' in test:   
        test = test.replace('  ', ' ')
    return test

def tokenize_and_rebuild(text):
    """
    docstring
    """
    tests = word_tokenize(text)
    return tests

def unicode_to_str(text):
    """
    docstring
    """
    if isinstance(text, unicode):
        return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore')

if __name__ == "__main__":
    text = 'Is      there a way to make     Firefox ignore invalid ssl-certificates?'
    print(preprocess_question(text))
   