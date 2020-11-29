# To install the NLTK Python Library:  pip install --user -U nltk
from nltk.tokenize import word_tokenize
import re


def preprocess_question(question):
    """
    This method does the preprocessing of Questions
    from the Database
    param: Question - The Question object to be preprocessed
    return: returns the Question Object
    """
    # question.title = preprocess_title(question.title)
    question = preprocess_body(question)
    # question.body = preprocess_body(question.body)
    # question.tag = preprocess_tag(question.tag)
    return question


def preprocess_title(title):
    """
    This method makes the text lower, removes white space and rebuilds the
    titles text
    """
    test_data = title.lower()
    test_data = remove_double_space(test_data.replace('\n', ' '))
    test_data = tokenize(test_data)
    return test_data


def remove_double_space(test):
    while '  ' in test:
        test = test.replace('  ', ' ')
    return test


def tokenize(test):
    """
    docstring
    """
    test_data = word_tokenize(test)
    return test_data


def preprocess_body(body_data):
    """
    preprocess_body: This method will Preprocess text from the
    body of the Posts we get from the db
    @return: tokenized data object
    @rtype:
    """
    test_data = body_data.lower()
    test_data = clean_pre_tags(test_data)
    test_data = clean_html_tags(test_data)
    test_data = remove_double_space(test_data.replace('\n', ' '))
    test_data = tokenize(test_data)
    cv_list = []
    if test_data:
        for element in test_data:
            cv_list.append(element.strip())
        return cv_list
    else:
        return ''


def clean_pre_tags(test_data):
    pre_regex = r'<pre(.*?)><code>([\s\S]*?)</code></pre>'
    # The string is scanned left-to-right, and matches are returned in the order found.
    # Empty matches are included in the result.
    for match in re.finditer(pattern=pre_regex, string=test_data):
        start_index = match.start()
        end_index = match.end()
        data = test_data[start_index:end_index]
        test_data = test_data.replace(data, " ")
        test_data = test_data.replace('\n', ' ')
    return test_data


def clean_html_tags(test_data):
    """
    clean_html_tags: This method removed all the html tags using regular
    expressions
    @note: this can also be done using python BeautifySoup
cleaned text without HTML tags
    @rtype:
    """
    html_regex = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    cleaned_html = re.sub(html_regex, '', test_data)
    return cleaned_html


def preprocess_tag(tag):
    """
    preprocess_tag: this method will tokenize the tags
    @param tag: The tag object to be tokenized
    @type tag:
    @return: the tag object that is clean
    @rtype:
    """
    return tag.replace('<', ' ').replace('>', ' ').strip().split()

if __name__ == "__main__":
    #text = 'Is      there a way to make     Firefox ignore invalid ssl-certificates?'
    text = '<p>A long text........ </p>'
    print(preprocess_question(text))
