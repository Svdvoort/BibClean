import bibclean.utils.cleaning as cleaner
import bibclean.utils.formatting as formatter
import bibclean.config.constants as constants
from bibtexparser.customization import splitname
from Levenshtein import distance as levenshtein_distance
import requests
from crossref.restful import Works, Etiquette
import bibclean.crossref_tools.parser as cr_parser
import bibclean.bib_tools.parser as bib_parser
from bibclean.updating.general import update_field


def crossref_is_similar(cr_info, bib_info, max_levenshtein_distance):
    is_similar = False
    if cr_parser.has_title(cr_info):
        entry_title = bib_parser.get_title(bib_info)
        entry_title = cleaner.clean_braces(entry_title)
        crossref_title = cr_parser.get_title(cr_info)
        lev_distance = levenshtein_distance(crossref_title,
                                            entry_title)
        if lev_distance <= max_levenshtein_distance:
            is_similar = True

    return is_similar


def set_doi(entry, doi, update_URL):
    doi = cleaner.clean_doi(doi)
    entry = update_field(entry, 'doi', doi)
    if update_URL:
        new_url = formatter.format_doi_url(doi)
        entry = update_field(entry, 'url', new_url)

    return entry


def get_doi(entry, config):
    has_doi = bib_parser.has_doi(entry)
    my_etiquette = Etiquette(constants.PROJECT_NAME,
                             constants.VERSION,
                             constants.URL,
                             constants.EMAIL)
    max_levenshtein_distance = config.get_max_levenshtein_distance()
    update_URL = config.get_update_URL()

    works = Works(etiquette=my_etiquette)

    if not has_doi and bib_parser.has_url(entry):
        entry_url = bib_parser.get_url(entry)
        if 'doi' in entry_url:
            doi = cleaner.clean_doi(entry_url)

            if is_crossref_work(doi):
                crossref_info = works.doi(doi)
                if crossref_is_similar(crossref_info, entry,
                                       max_levenshtein_distance):
                    entry = set_doi(entry, doi, update_URL)
                    has_doi = True

    if not has_doi:
        # we try to find the doi for the title
        entry_title = bib_parser.get_title(entry)
        entry_title = cleaner.clean_braces(entry_title)
        author = bib_parser.get_author(entry)
        first_author = splitname(author[0], strict_mode=False)
        first_author_last_name = first_author['last'][0]

        query_parameters = {'author': first_author_last_name,
                            'bibliographic': entry_title}

        works_query = works.query(**query_parameters)
        works_query = works_query.sort('score').order('desc').select(['title',
                                                                      'DOI'])
        i_i_item = 0
        max_items = min(works_query.count(), 10)
        works_results = iter(works_query)
        while i_i_item < max_items and not has_doi:
            i_item = next(works_results)
            if crossref_is_similar(i_item, entry,
                                   max_levenshtein_distance):
                doi = cr_parser.get_doi(i_item)
                entry = set_doi(entry, doi, update_URL)
                has_doi = True
            i_i_item += 1
    else:
        # We check to see if the doi is correct
        doi = bib_parser.get_doi(entry)
        doi = cleaner.clean_doi(doi)
        if is_crossref_work(doi):
            crossref_info = works.doi(doi)

            if crossref_is_similar(crossref_info, entry,
                                   max_levenshtein_distance):
                entry = set_doi(entry, doi, update_URL)
            else:
                entry.pop('doi', None)
                if 'doi' in bib_parser.get_url(entry):
                    entry.pop('url', None)
                has_doi = False

        else:
            entry = set_doi(entry, doi, update_URL)

    return entry, has_doi


def is_crossref_work(doi):
    my_etiquette = Etiquette(constants.PROJECT_NAME,
                             constants.VERSION,
                             constants.URL,
                             constants.EMAIL)

    return Works(etiquette=my_etiquette).doi_exists(doi)


def get_doi_bib(doi):
    """
    Return a bibTeX string of metadata for a given DOI.
    From: https://gist.github.com/jrsmith3/5513926
    """

    url = constants.DOI_URL + doi

    headers = {"accept": "application/x-bibtex"}
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        bib = r.text
    else:
        bib = None
    return bib
