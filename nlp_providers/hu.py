import sys

import huspacy
import spacy
from spacy import Language


def get_hungarian_npl_model() -> Language:
    try:
        nlp = huspacy.load()
    except OSError:
        print("Can't find model 'hu_core_news_lg'. Trying to download and install it."
              " Please, wait a few seconds." )
        huspacy.download()
        nlp = huspacy.load()
    return nlp


def get_german_npl_model() -> Language:
    try:
        nlp = spacy.load('de_dep_news_trf')
    except OSError:
        print("Can't find model 'de_dep_news_trf'. Trying to download and install it."
              " Please, wait a few seconds." )
        download_model('de_dep_news_trf')
        nlp = spacy.load('de_dep_news_trf')
    return nlp


def download_model(model_name: str) -> None:
    cmd = [sys.executable, "-m", "spacy", "download"] + [model_name]
    spacy.util.run_command(cmd)
