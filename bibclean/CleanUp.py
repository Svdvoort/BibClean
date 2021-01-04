import logging
import bibclean.utils.cleaning as cleaner
import bibclean.utils.convert as converter
import bibclean.utils.formatting as formatter
from bibclean.config import ConfigLoader
from bibclean.IO import loaders, writers, ArgParser
from bibclean.utils import doi_tools
from crossref.restful import Works
import hashlib
import json
import nltk


def get_entry_type(type_info):
    entry_type_table = {
        "proceedings-article": "inproceedings",
        "journal-article": "article",
        "book-chapter": "inbook",
        "proceedings": "proceedings",
    }

    entry_type = entry_type_table[type_info]
    return entry_type


def get_entry_hash(entry):
    entry_copy = entry.copy()
    entry_copy["ID"] = "temp"
    entry_string = json.dumps(entry_copy, sort_keys=True).encode("utf-8")
    entry_hash = hashlib.md5(entry_string).hexdigest()
    return entry_hash


def process_bib(config_file=None, input_file=None, output_file=None):
    nltk.download("punkt")

    if config_file is None:
        argreader = ArgParser.ArgReader()
        config_file = argreader.get_config_file()

    works = Works()

    logging.basicConfig(
        format="%(levelname)-8s %(message)s", level=logging.INFO, filename="out.log"
    )
    logger = logging.getLogger(__name__)

    config = ConfigLoader.ConfigLoader(config_file)
    config.input_bib_file = input_file
    config.output_bib_file = output_file

    bib_file = config.input_bib_file
    out_bib_file = config.output_bib_file
    max_authors = config.get_max_authors()
    remove_duplicates = config.get_remove_duplicates()

    bib_database = loaders.load_bibtex_file(bib_file)

    hashes = {}
    new_entries = ()

    for entry in bib_database.entries:
        print(entry["ID"])
        entry, has_doi = doi_tools.get_doi(entry, config)
        if has_doi:
            if doi_tools.is_crossref_work(entry["doi"]):

                entry_info = works.doi(entry["doi"])

                entry = converter.json_to_bib(entry_info, entry, config)

                # entry_type = get_entry_type(entry_info['type'])

            else:
                doi_org_info = doi_tools.get_doi_bib(entry["doi"])

                if doi_org_info is not None:
                    entry_info = loaders.load_bibtex_string(doi_org_info)

                    entry_info = entry_info.entries[0]

                    entry = converter.bib_to_bib(entry_info, entry, config)
                else:
                    warning_invalid_doi_string = (
                        "Entry {entry_id} has an invalid doi {doi}; removed DOI"
                    )
                    logging.warning(
                        warning_invalid_doi_string.format(entry_id=entry["ID"], doi=entry["doi"])
                    )
                    entry.pop("doi", None)
                    has_doi = False

        if not has_doi:
            entry["author"] = formatter.format_author_list(entry["author"])

        entry["title"] = cleaner.clean_text(entry["title"])
        entry["author"] = formatter.name_list_to_bib(entry["author"], max_authors)

        if "editor" in entry:
            entry["editor"] = formatter.name_list_to_bib(entry["editor"], max_authors)

        entry_hash = get_entry_hash(entry)
        if entry_hash not in hashes:
            hashes[entry_hash] = entry["ID"]
            new_entries.append(entry)
        else:
            inf_string = "Entry {} seems to be the same as {}"

            if remove_duplicates:
                inf_string = inf_string + " ; removed entry {}"
                msg = inf_string.format(entry["ID"], hashes[entry_hash], entry["ID"])
                logger.warning(msg)
            else:
                msg = inf_string.format(entry["ID"], hashes[entry_hash])
                logger.warning(msg)
                new_entries.append(entry)

    bib_database.entries = new_entries
    writers.write_bibtex_file(bib_database, out_bib_file)


if __name__ == "__main__":
    process_bib()
