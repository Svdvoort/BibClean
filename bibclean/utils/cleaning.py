import string
from pylatexenc import latexencode
import idutils
import numpy as np
from bibtexparser.customization import splitname
from bibclean.config import constants
import bibclean.utils.formatting as formatter
import re
import nltk
import wordninja
from nltk.tokenize.treebank import TreebankWordDetokenizer



def clean_braces(text):
    return text.replace(constants.L_BRACE, '').replace(constants.R_BRACE, '')


def enclose_braces(text):
    text = clean_braces(text)
    return constants.L_BRACE + text + constants.R_BRACE


def clean_unicode(text):
    clean_text = ''
    for i_character in text:
        encoded_character = latexencode.unicode_to_latex(i_character)

        if len(encoded_character) > 1 and (encoded_character[0] != constants.L_BRACE or encoded_character[-1] != constants.R_BRACE):
            encoded_character = encoded_character.replace(constants.R_BRACE, '').split(constants.L_BRACE)
            encoded_character = ' '.join(encoded_character)
            encoded_character = enclose_braces(encoded_character)

        clean_text += encoded_character

    return clean_text


def clean_doi(doi):
    doi = idutils.normalize_doi(doi)
    doi = doi.replace('\\', '')
    return doi


def clean_text(text):
    text = clean_braces(text)
    text_elements = nltk.word_tokenize(text)
    out_elements = []
    for i_element in text_elements:
        sub_elements = wordninja.split(i_element)
        if len(sub_elements) == 0 or len(sub_elements) == 1:
            out_elements.append(i_element)
        elif len(sub_elements) > 1 and all([len(i_element) > 1 for i_element in sub_elements]):
            out_elements.extend(sub_elements)
        elif len(sub_elements) > 1:
            out_elements.append(i_element)
    text_elements = out_elements



    new_text_elements = list()
    for i_element in text_elements:
        i_element = clean_unicode(i_element)

        N_required = 2
        is_uppercase_char = [1 if c.isupper() else 0 for c in i_element]
        N_upper_case = sum(is_uppercase_char)
        is_punctuation_char = [i_char in string.punctuation for i_char in i_element]
        contains_punctuation = any(is_punctuation_char)
        is_digit = [i_char in string.digits for i_char in i_element]
        contains_digit = any(is_digit)

        if N_upper_case >= N_required and not contains_punctuation:
            i_element = enclose_braces(i_element)
        elif N_upper_case >= N_required and i_element[0] in string.punctuation and i_element[-1] in string.punctuation:
            i_element = i_element[0] + enclose_braces(i_element[1:-1]) + i_element[-1]
        elif N_upper_case >= N_required and i_element[-1] in string.punctuation:
            i_element = enclose_braces(i_element[0:-1]) + i_element[-1]
        elif N_upper_case >= N_required and i_element[0] in string.punctuation:
            i_element = i_element[0] + enclose_braces(i_element[1:])
        elif N_upper_case >= N_required:
            uppercase_location = np.argwhere(is_uppercase_char)
            punctuation_location = np.argwhere(is_punctuation_char)

            if len(uppercase_location) > len(punctuation_location) + 1:
                if i_element[-1] in string.punctuation:
                    i_element = enclose_braces(i_element[0:-1]) + i_element[-1]
                else:
                    i_element = enclose_braces(i_element)
            elif len(uppercase_location) == len(punctuation_location) + 1:
                for i_punctuation_location in punctuation_location:
                    if (i_punctuation_location + 1) not in uppercase_location:
                        # Special case, since the capital does not follow directly after the punctuation
                        # We assume that we thus need to keep capitalization
                        i_element = enclose_braces(i_element)
                        break

        if contains_digit and N_upper_case >= 1:
            i_element = enclose_braces(i_element)

        new_text_elements.append(i_element)

    out_text = TreebankWordDetokenizer().detokenize(new_text_elements)
    return out_text


def clean_institute_author(author):
    author = author.split(constants.R_BRACE)
    is_institute = False
    if len(author) > 1:
        if author[1][2] == constants.L_BRACE:
            author = enclose_braces(author[1].split(constants.L_BRACE)[1] + ' ' + author[0])
            is_institute = True
    return author, is_institute


def clean_name(author):
    if type(author) == dict:
        if 'name' in author:
            out_author = clean_text(author['name'].strip())
            out_author = enclose_braces(out_author)
            return out_author
        if 'given' in author and 'family' in author:
            given_name = author['given']
            family_name = author['family']
            full_name = given_name + ' ' + family_name
            name_parts = splitname(full_name)
        elif 'given' in author:
            full_name = author['given']
            print('Check me: ' + full_name)
            name_parts = splitname(full_name)
        elif 'family' in author:
            full_name = author['family']
            print('Check me: ' + full_name)
            name_parts = splitname(full_name)
        else:
            print(author)
            out_author = clean_text(author['name'].strip())
            out_author = enclose_braces(out_author)
            return out_author
    elif type(author) == str:
        institute_author, is_institute = clean_institute_author(author)
        if is_institute:
            return institute_author

        author = clean_braces(author)
        name_parts = splitname(author)
    else:
        raise Exception('Unknown author type!')

    out_author = formatter.format_author_name(name_parts)

    return out_author
