#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re

from pathlib import Path
from typing import Optional

import questionary
import typer

from fastapi_ccli import __version__
from fastapi_ccli.cloner.cloner_en import exec_clone, is_china
from fastapi_ccli.utils.get_path import get_project_path

app_en_form = typer.Typer(rich_markup_mode='rich')


@app_en_form.command(epilog='Made by :beating_heart: wu-clan')
def cloner(
    version: Optional[bool] = typer.Option(
        None,
        '--version',
        '-V',
        help='Print version information.',
    ),
    project_path: Optional[str] = typer.Option(
        None,
        '--path',
        '-p',
        metavar='<PATH>',
        show_default=False,
        help="Project clone path, the default is '../fastapi_project', supports absolute path or relative path.",
    ),
):
    """
    FastAPI project cloner
    """
    if version:
        typer.secho('\n🔥 FastAPI CCLI ' + __version__, fg='green', bold=True)
    if project_path:
        if not Path(project_path).is_dir():
            raise typer.BadParameter('Wrong parameter input, please enter the correct path')
        use_project_name = project_path or '../fastapi_project'
        path = get_project_path(use_project_name)
        project_name = re.split(r'/|\'|\\|\\\\', use_project_name)[-1]
        result_if = questionary.form(
            orm=questionary.select(
                'Please select the orm you want to use:',
                choices=['sqlalchemy', 'tortoise', 'sqlmodel'],
                default='sqlalchemy',
            ),
            country=questionary.select('Is your region China?', choices=['Yes', 'No'], default='No'),
        ).ask()
        if len(result_if) == 0:
            raise typer.Exit(1)
        country = is_china(result_if['country'])
        orm = result_if['orm']
        exec_clone(orm, country, project_name, path)
