import bibtexparser
from bibtexparser.bwriter import BibTexWriter


def write_bibtex_file(bib_database, filepath):
    writer = BibTexWriter()
    writer.contents = ['entries']
    writer.indent = '\t'
    writer.align_values = True

    with open(filepath, 'w') as bibtex:
        bibtexparser.dump(bib_database, bibtex, writer)
