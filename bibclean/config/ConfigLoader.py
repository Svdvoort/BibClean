import yaml


class ConfigLoader:
    def __init__(self, config_file):
        self.config_file = config_file
        with open(config_file, "r") as ymlfile:
            self.cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

        self._input_bib_file = None
        self._output_bib_file = None

        self.input_bib_file = None
        self.output_bib_file = None

    @property
    def input_bib_file(self):
        return self._input_bib_file

    @input_bib_file.setter
    def input_bib_file(self, value):
        if value is None:
            self._input_bib_file = self.cfg["file_paths"]["input_bib_file"]
        else:
            self._input_bib_file = value

    @property
    def output_bib_file(self):
        return self._output_bib_file

    @output_bib_file.setter
    def output_bib_file(self, value):
        if value is None:
            self._output_bib_file = self.cfg["file_paths"]["output_bib_file"]
        else:
            self._output_bib_file = value

    def get_max_authors(self):
        return self.cfg["appearance"]["max_authors"]

    def get_max_levenshtein_distance(self):
        return self.cfg["max_levenshtein_distance"]

    def get_update_authors(self):
        return self.cfg["update_fields"]["update_authors"]

    def get_update_date(self):
        return self.cfg["update_fields"]["update_date"]

    def get_update_container(self):
        return self.cfg["update_fields"]["update_container"]

    def get_update_publisher(self):
        return self.cfg["update_fields"]["update_publisher"]

    def get_update_editors(self):
        return self.cfg["update_fields"]["update_editors"]

    def get_remove_duplicates(self):
        return self.cfg["remove_duplicate_entries"]

    def get_update_ISSN(self):
        return self.cfg["update_fields"]["update_ISSN"]

    def get_update_ISBN(self):
        return self.cfg["update_fields"]["update_ISBN"]

    def get_update_URL(self):
        return self.cfg["update_fields"]["update_URL"]

    def get_update_pages(self):
        return self.cfg["update_fields"]["update_pages"]

    def get_article_number_keyword(self):
        return self.cfg["article_number_keyword"]

    def get_article_number_remove_pages(self):
        return self.cfg["article_number_remove_pages"]

    def get_update_title(self):
        return self.cfg["update_fields"]["update_title"]

    def get_update_article_number(self):
        return self.cfg["update_fields"]["update_article_number"]

    def get_update_doi(self):
        return self.cfg["update_fields"]["update_doi"]

    def get_update_volume(self):
        return self.cfg["update_fields"]["update_volume"]

    def get_update_issue(self):
        return self.cfg["update_fields"]["update_issue"]
