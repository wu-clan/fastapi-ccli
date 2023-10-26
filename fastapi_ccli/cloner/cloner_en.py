#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re
import time
from pathlib import Path
from typing import Optional

import typer
from rich import print

from fastapi_ccli import __version__
from fastapi_ccli.cloner import GREEN, RED, github_fba_src, github_ftm_src, github_fsm_src, gitee_fba_src, gitee_ftm_src
from fastapi_ccli.utils.get_country import get_current_country
from fastapi_ccli.utils.get_ip import get_net_ip
from fastapi_ccli.utils.get_path import get_project_path

app_en = typer.Typer(rich_markup_mode="rich")


def is_china(dns: bool) -> str:
    """
    Whether to use dns

    :param dns:
    :return:
    """
    with typer.progressbar(range(5), label="Analyzing") as progress:
        for i in progress:
            ip = get_net_ip()
            if ip:
                progress.update(5)
                break
            else:
                time.sleep(0.3)
                progress.update(i)
                continue
        rp = get_current_country(ip)
        if "CN" in rp:
            ending = GREEN if dns else RED
        else:
            ending = RED if dns else GREEN
        return ending


def exec_clone(orm: str, country: str, project: str, path: str) -> None:
    """
    Perform clone

    :param orm:
    :param country:
    :param project:
    :param path:
    :return:
    """
    typer.echo("Project name: " + typer.style(project, fg="blue", bold=True))
    typer.echo("Select orm: " + orm)
    if orm == "sqlalchemy":
        source = github_fba_src if "True" in country else gitee_fba_src
    elif orm == "tortoise":
        source = github_ftm_src if "True" in country else gitee_ftm_src
    elif orm == "sqlmodel":
        source = github_fsm_src
    try:
        print(f"⏳ Start clone {source.split('/')[-1].split('.')[0]} project...")  # noqa
        out = os.system(f"git clone {source} {path}")
        if out != 0:
            raise RuntimeError(out)
    except Exception as e:
        print(f"❌ Clone project failed: {e}")
        raise typer.Exit(1)
    else:
        print("✅ The project was cloned successfully")
        typer.echo(f"Please go to the directory {typer.style(path, fg='green', bold=True)} to view")


@app_en.command(epilog="Made by :beating_heart: wu-clan")
def cloner(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-V",
        help="Print version information.",
    ),
    orm: Optional[str] = typer.Option(
        "sqlalchemy",
        "--orm",
        "-o",
        metavar="<ORM>",
        help="Select the orm to use, the default is sqlalchemy, support 'sqlalchemy' / 'tortoise' / 'sqlmodel'.",
    ),
    project_path: Optional[str] = typer.Option(
        None,
        "--path",
        "-p",
        metavar="<PATH>",
        show_default=False,
        help="Project clone path, the default is '../fastapi_project', supports absolute path or relative path.",
    ),
):
    """
    FastAPI project cloner
    """
    if version:
        typer.secho("\n🔥 FastAPI CCLI " + __version__, fg="green", bold=True)
    if orm:
        if orm not in ["sqlalchemy", "tortoise", "sqlmodel"]:
            raise typer.BadParameter("Enter unknown parameters, only allowed 'sqlalchemy' / 'tortoise' / 'sqlmodel'")
    if project_path:
        if not Path(project_path).is_dir():
            raise typer.BadParameter("Wrong parameter input, please enter the correct path")
        use_project_name = project_path or "../fastapi_project"
        path = get_project_path(use_project_name)
        project_name = re.split(r"/|\'|\\|\\\\", use_project_name)[-1]
        _country = typer.confirm("Is your region China?", default=False)
        country = is_china(_country)
        exec_clone(orm, country, project_name, path)
