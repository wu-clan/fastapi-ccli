#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys

import questionary

from fastapi_ccli.cloner.en.cloner_en import app_en
from fastapi_ccli.cloner.en.cloner_en_form import app_en_form
from fastapi_ccli.cloner.version import version
from fastapi_ccli.cloner.zh.cloner_zh import app_zh
from fastapi_ccli.cloner.zh.cloner_zh_form import app_zh_form


def main():
    if len(sys.argv) > 1:
        if any(sys.argv[1] == _ for _ in ['--version', '-V']):
            version()
    select_language = questionary.form(
        language=questionary.select('Please select your language:', choices=['zh-hans', 'en'], default='en')
    ).ask()
    if len(select_language) == 0:
        sys.exit(0)
    elif select_language['language'] == 'zh-hans':
        select_run_type = questionary.form(
            interactive=questionary.select('是否以交互模式运行?', choices=['yes', 'no'], default='yes')
        ).ask()
        if len(select_run_type) == 0:
            sys.exit(0)
        if select_run_type.get('interactive') == 'yes':
            app_zh_form()
        else:
            app_zh()
    else:
        select_run_type = questionary.form(
            interactive=questionary.select('Whether to run in interactive mode?', choices=['yes', 'no'], default='yes')
        ).ask()
        if len(select_run_type) == 0:
            sys.exit(0)
        if select_run_type.get('interactive') == 'yes':
            app_en_form()
        else:
            app_en()
