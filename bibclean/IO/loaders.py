import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser import customization


def editor(record):
    """
    Split editor field into a list of "Name, Surname".

    :param record: the record.
    :type record: dict
    """
    if "editor" in record:
        if record["editor"]:
            record["editor"] = customization.getnames(
                [i.strip() for i in record["editor"].replace("\n", " ").split(" and ")]
            )
        else:
            del record["editor"]
    return record


def customizations(record):
    """Use some functions delivered by the library

    :param record: a record
    :returns: -- customized record
    """
    # record = homogenize_latex_encoding(record)
    # record = customization.type(record)
    record = customization.author(record)
    record = editor(record)
    # record = editor(record)
    # # print(record)
    # # This makes it a dict
    # # record = journal(record)
    # # print(record)
    # record = keyword(record)
    # record = link(record)
    record = customization.page_double_hyphen(record)
    # record = doi(record)
    return record


def load_bibtex_file(filepath):
    parser = BibTexParser(common_strings=True, ignore_nonstandard_types=True)
    parser.customization = customizations

    with open(filepath, "r") as bibtex:
        bib_database = bibtexparser.load(bibtex, parser=parser)

    return bib_database


def load_bibtex_string(string):
    string_parser = BibTexParser(common_strings=True, ignore_nonstandard_types=True)
    string_parser.customization = customizations

    bib_database = bibtexparser.loads(string, parser=string_parser)

    return bib_database
