import logging

logger = logging.getLogger(__name__)


def update_field(bib_entry, field_name, value):
    if field_name not in bib_entry or bib_entry[field_name] != value:
        logger.info('Changed field {} for {}'.format(field_name,
                                                     bib_entry['ID']))
        if field_name == 'author' and len(value) < len(bib_entry['author']):
            logger.warning('Removed authors from {}'.format(bib_entry['ID']))
        bib_entry[field_name] = value
    return bib_entry
