#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import typer

from app.CN.cloner_zh import app_zh
from app.CN.cloner_zh_ic import app_zh_ic
from app.EN.cloner_en import app_en
from app.EN.cloner_en_ic import app_en_ic


def main():
    interactive = typer.confirm('是否以交互模式运行(whether to run in interactive mode)?', default=True)
    language = typer.confirm('是否开启命令行中文提示(Whether to enable the command line Chinese prompt)?', default=True)
    if interactive:
        if language:
            app_zh_ic()
        else:
            app_en_ic()
    else:
        if language:
            app_zh()
        else:
            app_en()


if __name__ == '__main__':
    main()
