import bibclean.utils.cleaning as cleaner
import bibclean.crossref_tools.parser as parser
import bibclean.crossref_tools.api_caller as caller
from bibclean.updating.general import update_field


def update_authors(cr_info, bib_entry):
    authors = parser.get_author(cr_info)
    authors = [cleaner.clean_name(i_author) for i_author in authors]

    bib_entry = update_field(bib_entry, "author", authors)

    return bib_entry


def update_editors(cr_info, bib_entry):
    editors = None
    if parser.has_ISBN(cr_info):
        isbn = parser.get_ISBN(cr_info)

        editors = caller.get_editors_from_ISBN(isbn, cr_info["type"])
    elif parser.has_editor(cr_info):
        editors = parser.get_editor(cr_info)

    if editors is not None:
        editors = [cleaner.clean_name(i_editor) for i_editor in editors]
        bib_entry = update_field(bib_entry, "editor", editors)
    return bib_entry


def update_container(cr_info, bib_entry):
    if parser.has_container_title(cr_info):
        container_title = parser.get_container_title(cr_info)
        if bib_entry["ENTRYTYPE"] == "article":
            main_field_name = "journal"
            sub_field_name = "journalsubtitle"
        else:
            main_field_name = "booktitle"
            sub_field_name = "booksubtitle"

        main_title = container_title[0]
        main_title = cleaner.clean_text(main_title)
        bib_entry = update_field(bib_entry, main_field_name, main_title)

        if len(container_title) > 1:
            sub_title = container_title[1]
            sub_title = cleaner.clean_text(sub_title)
            bib_entry = update_field(bib_entry, sub_field_name, sub_title)

    return bib_entry


def update_ISBN(cr_info, bib_entry):
    if parser.has_ISBN(cr_info):
        ISBN = parser.get_ISBN(cr_info)
        bib_entry = update_field(bib_entry, "isbn", ISBN)
    return bib_entry


def update_publisher(cr_info, bib_entry):
    publisher_name = None

    if parser.has_member_ID(cr_info):
        member_ID = parser.get_member_ID(cr_info)
        publisher_name = caller.get_publisher_name_from_ID(member_ID)
    elif parser.has_publisher(cr_info):
        publisher_name = parser.get_publisher(cr_info)

        if caller.publisher_has_member_ID(publisher_name):
            member_ID = caller.get_member_ID_from_publisher(publisher_name)
            publisher_name = caller.get_publisher_name_from_ID(member_ID)

    if publisher_name is not None:
        publisher_name = cleaner.clean_text(publisher_name)
        bib_entry = update_field(bib_entry, "publisher", publisher_name)
    return bib_entry


def update_date(cr_info, bib_entry):
    if parser.has_publication_date(cr_info):
        date = parser.get_publication_date(cr_info)
        if "year" in date:
            year = date["year"]
            bib_entry = update_field(bib_entry, "year", year)
        if "month" in date:
            month = date["month"]
            bib_entry = update_field(bib_entry, "month", month)
        if "day" in date:
            day = date["day"]
            bib_entry = update_field(bib_entry, "day", day)
    return bib_entry


def update_title(cr_info, bib_entry):
    if parser.has_title(cr_info):
        title = parser.get_title(cr_info)
        title = cleaner.clean_text(title)

        bib_entry = update_field(bib_entry, "title", title)

    return bib_entry


def update_ISSN(cr_info, bib_entry):
    if parser.has_ISSN(cr_info):
        issn = parser.get_ISSN(cr_info)

        bib_entry = update_field(bib_entry, "issn", issn)

    return bib_entry


def update_pages(cr_info, bib_entry):
    if parser.has_pages(cr_info):
        pages = parser.get_pages(cr_info)
        bib_entry = update_field(bib_entry, "pages", pages)

    return bib_entry


def update_article_number(cr_info, bib_entry, keyword="pages", remove_pages=False):
    if parser.has_article_number(cr_info):
        article_number = parser.get_article_number(cr_info)
        article_number = cleaner.clean_text(article_number)
        bib_entry = update_field(bib_entry, keyword, article_number)

        if remove_pages and keyword != "pages":
            bib_entry.pop("pages", None)

    return bib_entry


def update_doi(cr_info, bib_entry):
    if parser.has_doi(cr_info):
        doi = parser.get_doi(cr_info)
        doi = cleaner.clean_doi(doi)

        bib_entry = update_field(bib_entry, "doi", doi)

    return bib_entry


def update_volume(cr_info, bib_entry):
    if parser.has_volume(cr_info):
        volume = parser.get_volume(cr_info)

        bib_entry = update_field(bib_entry, "volume", volume)

    return bib_entry


def update_issue(cr_info, bib_entry):
    if parser.has_issue(cr_info):
        issue = parser.get_issue(cr_info)

        bib_entry = update_field(bib_entry, "issue", issue)

    return bib_entry
