def has_doi(bib_info):
    return 'doi' in bib_info


def get_doi(bib_info):
    return bib_info['doi']


def has_title(bib_info):
    return 'title' in bib_info


def get_title(bib_info):
    return bib_info['title']


def has_url(bib_info):
    return 'url' in bib_info


def get_url(bib_info):
    if 'url' in bib_info:
        return bib_info['url']
    else:
        return ''


def has_author(bib_info):
    return 'author' in bib_info


def get_author(bib_info):
    return bib_info['author']
