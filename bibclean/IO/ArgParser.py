import argparse


class ArgReader:
    def __init__(self):
        parser = argparse.ArgumentParser(description="BibClean helps you clean up your BibTex file")
        parser.add_argument(
            "--config", "-C", "-c", type=str, required=True, help="The config file for BibClean"
        )

        self.parser = parser
        self.parsed_args = self.parser.parse_args()
        return

    def get_config_file(self):
        return self.parsed_args.config
