import bibclean.updating.crossref_updating as cr_update
import bibclean.updating.bib_updating as bib_update
import bibclean.crossref_tools.parser as parser


def json_to_bib(json_entry, bib_entry, config):
    if config.get_update_authors():
        bib_entry = cr_update.update_authors(json_entry, bib_entry)

    if config.get_update_container():
        bib_entry = cr_update.update_container(json_entry, bib_entry)

    if config.get_update_date():
        bib_entry = cr_update.update_date(json_entry, bib_entry)

    if config.get_update_publisher():
        bib_entry = cr_update.update_publisher(json_entry, bib_entry)

    if config.get_update_editors():
        bib_entry = cr_update.update_editors(json_entry, bib_entry)

    if config.get_update_title():
        bib_entry = cr_update.update_title(json_entry, bib_entry)

    if config.get_update_ISSN():
        bib_entry = cr_update.update_ISSN(json_entry, bib_entry)

    if config.get_update_ISBN():
        bib_entry = cr_update.update_ISBN(json_entry, bib_entry)

    if config.get_update_pages():
        if parser.has_pages(json_entry):
            bib_entry = cr_update.update_pages(json_entry, bib_entry)
        elif (
            parser.has_article_number(json_entry) and config.get_article_number_keyword() == "pages"
        ):
            bib_entry = cr_update.update_article_number(
                json_entry, bib_entry, keyword="pages", remove_pages=False
            )
    if config.get_update_article_number():
        keyword = config.get_article_number_keyword()
        remove_pages = config.get_article_number_remove_pages()
        bib_entry = cr_update.update_article_number(
            json_entry, bib_entry, keyword=keyword, remove_pages=remove_pages
        )

    if config.get_update_doi():
        bib_entry = cr_update.update_doi(json_entry, bib_entry)

    if config.get_update_volume():
        bib_entry = cr_update.update_volume(json_entry, bib_entry)

    if config.get_update_issue():
        bib_entry = cr_update.update_issue(json_entry, bib_entry)

    return bib_entry


def bib_to_bib(new_bib_entry, original_bib_entry, config):
    if config.get_update_authors():
        original_bib_entry = bib_update.update_authors(new_bib_entry, original_bib_entry)

    return original_bib_entry
