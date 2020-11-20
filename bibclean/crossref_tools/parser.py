import numpy as np
import bibclean.config.constants as constants


def fix_text_encoding(text):
    # In some cases the text has been encoded in not utf-8
    # This is a problem for latex
    # So we try to solve it in this way

    to_try_encodings = ['iso-8859-1',
                        'windows-1251',
                        'windows-1252',
                        'shift-jis',
                        'gb2312',
                        'euc-kr',
                        'iso-8859-2',
                        'windows-1250',
                        'euc-jp',
                        'gbk',
                        'big5',
                        'iso-8859-15',
                        'iso-8859-9',
                        'windows-1256',
                        'latin-1']

    for i_to_try_encoding in to_try_encodings:
        try:
            text_encoded = text.encode(i_to_try_encoding)
            is_encoded = True
            break
        except UnicodeEncodeError:
            is_encoded = False

    if is_encoded:
        try:
            text = text_encoded.decode('utf-8')
        except UnicodeDecodeError:
            text = text
    else:
        text = text
    return text


def fix_encoding(item):
    if type(item) is str:
        item = fix_text_encoding(item)
    elif type(item) is list:
        item = [fix_encoding(i_text) for i_text in item]
    elif type(item) is dict:
        for key, value in item.items():
            item[key] = fix_encoding(value)
    return item


def has_ISBN(cr_info):
    return 'ISBN' in cr_info


def has_ISSN(cr_info):
    return 'ISSN' in cr_info


def get_ISBN(cr_info, preferred_type='print'):
    if 'isbn-type' in cr_info:
        isbn_info = cr_info['isbn-type']

        isbn_type = np.asarray([i_info['type'] for i_info in isbn_info])
        if preferred_type in isbn_type:
            preferred_index = np.squeeze(np.argwhere(isbn_type == preferred_type))
            isbn = isbn_info[preferred_index]['value']
        else:
            isbn = isbn_info[0]['value']

    elif 'ISBN' in cr_info:
        isbn = cr_info['ISBN'][0]

    else:
        isbn = None

    return isbn


def get_ISSN(cr_info, preferred_type='print'):
    if 'issn-type' in cr_info:
        issn_info = cr_info['issn-type']

        issn_type = np.asarray([i_info['type'] for i_info in issn_info])
        if preferred_type in issn_type:
            preferred_index = np.squeeze(np.argwhere(issn_type == preferred_type))
            issn = issn_info[preferred_index]['value']
        else:
            issn = issn_info[0]['value']

    elif 'issn' in cr_info:
        issn = cr_info['issn'][0]

    else:
        issn = None

    return issn


def has_journal_issue_date(cr_info):
    publication_types = constants.PUBLICATION_TYPES
    if 'journal-issue' in cr_info:
        journal_info = cr_info['journal-issue']

        for i_publication_type in publication_types:
            has_date = (i_publication_type in journal_info and
                        'date-parts' in journal_info[i_publication_type])
            if has_date:
                return has_date
    return False


def has_published_date(cr_info):
    publication_types = constants.PUBLICATION_TYPES
    for i_publication_type in publication_types:
        has_date = (i_publication_type in cr_info and
                    'date-parts' in cr_info[i_publication_type])
        if has_date:
            return has_date
    return False


def has_issued_date(cr_info):
    return ('issued' in cr_info and
            'date-parts' in cr_info['issued'])


def has_publication_date(cr_info):
    has_date = (has_journal_issue_date(cr_info) or
                has_published_date(cr_info) or
                has_issued_date(cr_info))

    return has_date


def get_publication_date(cr_info):
    publication_types = constants.PUBLICATION_TYPES

    if has_journal_issue_date(cr_info):
        journal_info = cr_info['journal-issue']
        for i_publication_type in publication_types:
            has_date = (i_publication_type in journal_info and
                        'date-parts' in journal_info[i_publication_type])
            if has_date:
                date_parts = journal_info[i_publication_type]['date-parts']
                break
    elif has_published_date(cr_info):
        for i_publication_type in publication_types:
            has_date = (i_publication_type in cr_info and
                        'date-parts' in cr_info[i_publication_type])
            if has_date:
                date_parts = cr_info[i_publication_type]['date-parts']
                break
    elif has_issued_date(cr_info):
        date_parts = cr_info['issued']['date-parts']
    else:
        err = 'Crossref data for DOI {} has no date!'.format(cr_info['DOI'])
        raise ValueError(err)

    date_parts = np.squeeze(date_parts)
    date = dict()
    N_date_parts = date_parts.size
    if N_date_parts == 1:
        date['year'] = str(date_parts)
    if N_date_parts >= 2:
        date['year'] = str(date_parts[0])
        month_number = date_parts[1]
        # Requires -1 for proper indexing
        date['month'] = constants.ENGLISH_MONTHS[month_number - 1]
    if N_date_parts >= 3:
        date['day'] = str(date_parts[2])
    return date


def has_container_title(cr_info, short=False):
    if not short:
        return 'container-title' in cr_info
    else:
        return 'short-container-title' in cr_info


def get_container_title(cr_info, short=False):
    if has_container_title(cr_info, short=short):
        if not short:
            container_title = cr_info['container-title']
        else:
            container_title = cr_info['short-container-title']
    else:
        err_str = 'Crossref dat for DOI {} has no container title!'
        raise KeyError(err_str.format(cr_info['DOI']))

    # TODO; sometimes container title exists of multiple parts
    # Give user the option to keep all of them
    # For now we just keep the first one

    # container_title = container_title[0]
    return fix_encoding(container_title)


def has_editor(cr_info):
    return 'editor' in cr_info


def get_editor(cr_info):
    return fix_encoding(cr_info['editor'])


def has_author(cr_info):
    return ('author' in cr_info and len(cr_info['author']) > 0)


def get_author(cr_info):
    return fix_encoding(cr_info['author'])


def has_publisher(cr_info):
    return 'publisher' in cr_info


def get_publisher(cr_info):
    return fix_encoding(cr_info['publisher'])


def has_member_ID(cr_info):
    return 'member' in cr_info


def get_member_ID(cr_info):
    return cr_info['member']


def has_title(cr_info):
    return ('title' in cr_info and len(cr_info['title']) > 0)


def get_title(cr_info):
    title = cr_info['title']
    # TODO; by default we get the first one, might want to change that
    if len(title) > 1:
        print(title)
    title = title[0]

    return fix_encoding(title)


def has_pages(cr_info):
    return 'page' in cr_info


def get_pages(cr_info):
    pages = cr_info['page']
    pages = pages.replace('-', '--')

    return pages


def has_article_number(cr_info):
    return 'article-number' in cr_info


def get_article_number(cr_info):
    return cr_info['article-number']


def has_doi(cr_info):
    return 'DOI' in cr_info


def get_doi(cr_info):
    return cr_info['DOI']


def has_volume(cr_info):
    return 'volume' in cr_info


def get_volume(cr_info):
    return cr_info['volume']


def has_issue(cr_info):
    has_issue = 'issue' in cr_info
    if not has_issue:
        if 'journal-issue' in cr_info and 'issue' in cr_info['journal-issue']:
            has_issue = True
    return has_issue


def get_issue(cr_info):
    if 'issue' in cr_info:
        issue = cr_info['issue']
    elif 'journal-issue' in cr_info and 'issue' in cr_info['journal-issue']:
        issue = cr_info['journal-issue']['issue']

    return issue
