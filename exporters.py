from __future__ import annotations

import time
from pathlib import Path

import jinja2
import pdfkit
from bingen.models import SkovorodaDict as SkvdDict_B
from sztaki.models import SkovorodaDict as SkvdDict_S


def export_html(skvd_dict: SkvdDict_B | SkvdDict_S):
    root = Path(__file__).parent.absolute()
    templateLoader = jinja2.FileSystemLoader(searchpath=root)
    templateEnv = jinja2.Environment(loader=templateLoader)
    template = templateEnv.get_template("template.html")

    outputText = template.render(skvd_dict=skvd_dict)

    html_file = open(str(int(time.time())) + '.html', 'w')
    html_file.write(outputText)
    html_file.close()


def export_pdf():
    for i in range(1,11):
        pdfkit.from_file(str(i) + '.html', str(i) + '.pdf')
