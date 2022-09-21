# Core module tokenizes a text, prepares lemmas.
import pathlib
import datetime
from typing import List, Set

import bingen
import sztaki
from bingen.translator import translate
from spacy import Language
from sztaki.translator import SztakiTranslator


def lemmatize_text(nlp: Language, text: str, lang: str) -> List[str]:
    doc = nlp(text)

    # Remove obsolete tokens
    doc = [token for token in doc if len(token.text) > 1]
    doc = [token for token in doc if not token.text[0].isdigit()]
    doc = [token for token in doc if not token.is_stop]
    doc = [token for token in doc if not token.is_punct]

    # Remove obsolete lemmas
    lemmas = [token.lemma_ for token in doc]
    lemmas = [lemma.strip() for lemma in lemmas]
    lemmas = [lemma for lemma in lemmas if len(lemma) > 1]
    lemmas = [lemma for lemma in lemmas if lemma.lower() not in get_custom_stopwords(lang=lang)]

    # Convert upper case lemmas to lower case
    for idx, lemma in enumerate(lemmas):
        if lemma.isupper():
            lemmas[idx] = lemma.lower()

    # Filter duplicates
    lemmas_unique = list()
    for lemma in lemmas:
        if lemma not in lemmas_unique:
            lemmas_unique.append(lemma)
    return lemmas_unique


def save_tokens_to_file(tokens: List[str], lang: str):
    tokens = "\n".join(tokens)
    date = datetime.datetime.now()
    filename = date.strftime("%Y-%m-%d-%H:%M_proto")
    root = pathlib.Path(__file__).parent.absolute()
    pathlib.Path(f'{root}/stopwords/{lang}/{filename}.txt').write_text(tokens, encoding='utf8')


def get_custom_stopwords(lang: str) -> Set[str]:
    root = pathlib.Path(__file__).parent.absolute()
    files = pathlib.Path(f'{root}/stopwords/{lang}').glob('*.txt')
    custom_stopwords = set()
    for filepath in files:
        if 'proto' not in filepath.name:
            text = filepath.read_text()
            words = text.split('\n')
            words = [word.strip().lower() for word in words]
            custom_stopwords.update(words)
    return  custom_stopwords


def translate_tokens(lang: str, tokens: List[str]):
    translation = None
    if lang == 'hu':
        translation = translate_hu_ua(tokens)
    elif lang == 'de':
        translation = translate_de_ua(tokens)
    return translation


def translate_hu_ua(tokens) -> sztaki.models.SkovorodaDict:
    translator = SztakiTranslator(dict_name='Stay In God\'s Love.',
                                  dict_description='Translated 4th chapter '
                                                   'of Hundatian version Stay '
                                                   'In God\'s Love',
                                  dict_language='Hungarian')
    for token in tokens:
        translator.translate_word_with_sztaki(token)
    # print(translator.sdict.to_dict())
    # print(translator.not_translated_words)
    return translator.sdict


def translate_de_ua(tokens) -> bingen.models.SkovorodaDict:
    sk_dict, not_translated_counter = translate(tokens)
    print(f'Not translated: {not_translated_counter}')
    print(sk_dict.to_dict())
    return sk_dict
