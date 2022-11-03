#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import typer
from fastapi_ccli import __version__

version = typer.Typer()


@version.command()
def print_version(
        _version: bool = typer.Option(
            True,
            '--version',
            '-V',
            help='获取当前框架版本号'
        )
):
    typer.secho(__version__, fg=typer.colors.WHITE, bold=True)
