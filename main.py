#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import typer

from app.cloner_en import app_en
from app.cloner_zh import app_zh


def main():
    language = typer.confirm('是否开启命令行中文提示(Whether to enable the command line Chinese prompt)?', default=True)
    if language:
        app_zh()
    else:
        app_en()


if __name__ == '__main__':
    main()
