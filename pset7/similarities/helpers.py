from nltk.tokenize import sent_tokenize


def lines(a, b):
    """Return lines in both a and b"""

    # TODO

    # Create list of lines in a then b
    a_list = a.splitlines()
    b_list = b.splitlines()
    matched_lines = set()

    # Iterate over lines in a
    for line in a_list:
        # Check for line in b_list
        if line in b_list:
            # Add line to matched_lines set
            matched_lines.add(line)

    return list(matched_lines)


def sentences(a, b):
    """Return sentences in both a and b"""

    # TODO

    # Create list of sentences in a then b
    a_list = sent_tokenize(a)
    b_list = sent_tokenize(b)
    matched_sentences = set()

    # Iterate over sentences in a_list
    for sentence in a_list:
        # Check for sentence in b_list
        if sentence in b_list:
            # Add sentence to matched_sentences set
            matched_sentences.add(sentence)

    return list(matched_sentences)


def substrings(a, b, n):
    """Return substrings of length n in both a and b"""

    # TODO

    def substring_list(s, n):
        """Convert a string into a list of substrings of length n"""
        j = 0
        sub_list = []
        for i in range(len(s) - n + 1):
            sub_list.append(s[i:(j + n)])
            j += 1
        return sub_list

    # Create list of substrings in a then b
    a_list = substring_list(a, n)
    b_list = substring_list(b, n)
    matched_substrings = set()

    # Iterate over substrings in a_list
    for substring in a_list:
        # Check for substring in b_list
        if substring in b_list:
            # Add substring to matched_substrings set
            matched_substrings.add(substring)

    return list(matched_substrings)