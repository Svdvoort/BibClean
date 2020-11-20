import os
import tempfile

from bibclean import CleanUp
from bibclean.IO import loaders

BIBLIOGRAPHY_TEST_DIR = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "test_data", "bibliographies",
)

BIBLIOGRAPHY_GROUNDTRUTH_DIR = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "test_data", "bibliographies_GT",
)

CONFIG_TEST_DIR = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "test_data", "configs",
)


def test_single_entry_pipeline():
    tmp_dir = tempfile.mkdtemp()
    config_file = os.path.join(CONFIG_TEST_DIR, "default_config.yaml")
    bib_file = os.path.join(BIBLIOGRAPHY_TEST_DIR, "einstein.bib")
    out_file = os.path.join(tmp_dir, "out.bib")
    groundtruth_bib_file = os.path.join(BIBLIOGRAPHY_GROUNDTRUTH_DIR, "einstein.bib")
    groundtruth_bib = loaders.load_bibtex_file(groundtruth_bib_file)

    CleanUp.process_bib(config_file, bib_file, out_file)
    processed_bib = loaders.load_bibtex_file(out_file)

    # Compare the output to the ground truth
    assert groundtruth_bib.entries_dict == processed_bib.entries_dict






