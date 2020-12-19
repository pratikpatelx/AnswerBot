class PatternHandler(object):
    """
    PatternHandler Class that implements the sematic patterns and the
    format patterns answer paragragraph content features
    """

    def get_semantic_pattern_value(self, ans_text):
        """
        get_semantic_pattern_value: This method calculates the semantic pattern values of sentences,
        if an answer paragraph contains alteast one of the semantic pattern we set the value to 1
        otherwise 0
        """
        Patterns = ['please check', 'pls check', 'you should', 'you can try', 'you could try', 'check out',
               'in short', 'the most important is', 'I d recommend', 'in summary', 'keep in mind that',
               'i suggest that']
        pattern_value = 0.0001

        for pattern in Patterns:
            if pattern in ans_text.lower():
                pattern_value = 1
        return pattern_value

    def get_format_pattern_value(self, ans_text):
        """
        get_format_pattern_value: This method calculates the the important HTML tags value
        used to emphasize the salient information in an answer paragraph. if an answer
        paragraph contains such HTML tags we set its format pattern score at 1 otherwise 0 
        """
        html_value = 0.0001

        HTML_Tag_bold = ['<strong>', '<code>']
        HTML_Tag_strike = ['<strike>']

        for tag in HTML_Tag_bold:
            if tag in ans_text.lower():
                html_value = 1
        for tag in HTML_Tag_strike:
            if tag in ans_text.lower():
                html_value = 1

        return html_value

if __name__ == "__main__":
    pattern = PatternHandler()
    pattern_test = 'Jupiter supports up to Eclipse 3.5. Jupiter Downloads Page '
    test = pattern.get_semantic_pattern_value(pattern_test)

    #html_test = "<strong>Hello World!</strong"
    html_test = "<strike>Hello World!</strike"
    temp = pattern.get_format_pattern_value(html_test)
    print(temp)