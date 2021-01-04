from bibclean.config import constants
from bibtexparser.customization import splitname
from bibclean.utils import cleaning as cleaner


def format_author_name(name_parts: dict):
    # author_name is already splitted author parts
    out_author = ""

    for i_part in name_parts["von"]:
        i_part = i_part.replace(".", "")
        i_part = cleaner.clean_unicode(i_part)
        out_author += i_part + " "

    for i_part in name_parts["last"]:
        i_part = i_part.replace(".", "")
        i_part = cleaner.clean_unicode(i_part)
        out_author += i_part
    out_author = out_author.strip()

    if len(name_parts["jr"]) > 0:
        out_author += ", "

    for i_part in name_parts["jr"]:
        i_part = cleaner.clean_unicode(i_part)
        out_author += i_part

    if len(name_parts["first"]) > 0:
        out_author += ", "

    print(name_parts["first"])
    for i_part in name_parts["first"]:
        print(i_part)
        i_part = i_part.replace(".", "")
        i_part = cleaner.clean_unicode(i_part) + " "
        print(i_part)
        out_author += i_part
        print(out_author)

    out_author = out_author.strip()
    return out_author


def format_author_list(authors):
    tidy_authors = []
    for i_author in authors:
        i_author = cleaner.clean_braces(i_author)
        author_name_parts = splitname(i_author, strict_mode=False)
        formatted_author = format_author_name(author_name_parts)

        tidy_authors.append(formatted_author)

    return tidy_authors


def name_list_to_bib(author_list, max_authors):
    if max_authors != constants.MAGIC_ANY and len(author_list) > max_authors:
        author_list = author_list[0:max_authors]
        author_list.append(constants.OTHERS_KEYWORD)

    return constants.AUTHOR_LINKING_KEYWORD.join(author_list)


def format_doi_url(doi):
    doi_url = constants.DOI_URL + doi
    return doi_url
