from core import save_tokens_to_file, lemmatize_text, get_custom_stopwords, translate_tokens
from pathlib import Path

from exporters import export_html
from nlp_providers.hu import get_german_npl_model

nlp = get_german_npl_model()

text = Path('de.txt').read_text(encoding='utf8')

tokens = lemmatize_text(nlp, text, lang='de')

save_tokens_to_file(tokens, lang='de')

translated = translate_tokens(lang='de', tokens=tokens)

export_html(translated)
