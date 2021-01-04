import bibclean.utils.cleaning as cleaner
from bibclean.updating.general import update_field


def update_authors(bib_info, bib_entry):
    author_list = [cleaner.clean_name(i_author) for i_author in bib_info["author"]]

    bib_entry = update_field(bib_entry, "author", author_list)

    return bib_entry
