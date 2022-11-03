#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re
import time
from typing import Optional

import typer
from rich import print

from fastapi_ccli import GREEN, RED, github_fs_src, gitee_fs_src, github_ft_src, gitee_ft_src
from fastapi_ccli.utils.get_country import get_current_country
from fastapi_ccli.utils.get_ip import get_net_ip
from fastapi_ccli.utils.get_path import get_project_path
from fastapi_ccli.utils.get_src import get_sqlalchemy_app_src

app_en = typer.Typer(rich_markup_mode="rich")


def orm_callback(orm: str) -> str:
    """
    Select the orm to use...

    :param orm:
    :return:
    """
    if orm:
        if orm == 'sqlalchemy' or orm == 's':
            use_orm = typer.style('sqlalchemy', fg='green', bold=True)
        elif orm == 'tortoise-orm' or orm == 't':
            use_orm = typer.style('tortoise-orm', fg='green', bold=True)
        else:
            raise typer.BadParameter(
                "Enter unknown parameters, only allowed 'sqlalchemy' / 's' or 'tortoise-orm' / 't'."
            )
    else:
        use_orm = typer.style('sqlalchemy', fg='green', bold=True)
    return use_orm


def project_path_callback(project_path: str) -> str:
    """
    Select project path...

    :param project_path:
    :return:
    """
    if project_path:
        if not isinstance(project_path, str):
            raise typer.BadParameter("Wrong parameter input, please enter the correct path")
        else:
            use_project_name = project_path
    else:
        use_project_name = '../fastapi_project'
    return use_project_name


def is_dns() -> str:
    dns = typer.confirm('Do you want to use dns?', default=False)
    with typer.progressbar(range(5), label='Analyzing') as progress:
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
        if 'CN' in rp:
            ending = GREEN if dns else RED
        else:
            ending = RED if dns else GREEN
        return ending


def is_async_app() -> str:
    async_app = typer.confirm('Do you want to use async?', default=True)
    ending = GREEN if async_app else RED
    return ending


def is_generic_crud() -> str:
    generic_crud = typer.confirm('Do you want to use generic crud?', default=True)
    ending = GREEN if generic_crud else RED
    return ending


def is_casbin() -> str:
    casbin = typer.confirm('Do you want to use rbac?', default=True)
    ending = GREEN if casbin else RED
    return ending


@app_en.command(epilog="Made by :beating_heart: wu-clan")
def cloner(
        _version: Optional[bool] = typer.Option(
            None,
            "--version",
            '-V',
            help="Print version information and quit"
        ),
        orm: Optional[str] = typer.Option(
            None,
            "--orm",
            "-o",
            callback=orm_callback,
            help="Select the orm to use, the default is sqlalchemy, support 'sqlalchemy' or 'tortoise-orm', "
                 "you can also use the shorthand, 's' or 't'."
        ),
        project_path: Optional[str] = typer.Option(
            None,
            "--path",
            "-p",
            callback=project_path_callback,
            help="Project clone path, the default is '../fastapi_project', supports absolute path or relative path, "
                 "E.g., Absolute path: D:\\fastapi_project, relative path: ../fastapi_project."
        ),
):
    """
    FastAPI project cloner
    """
    path = get_project_path(project_path)
    path_style = typer.style(path, fg='green', bold=True)
    project_name = re.split(r'/|\'|\\|\\\\', project_path)[-1]
    if 'sqlalchemy' in orm:
        dns = is_dns()
        async_app = is_async_app()
        generic_crud = is_generic_crud()
        casbin = None
        if 'True' in generic_crud:
            casbin = is_casbin()
        typer.echo('Project name: ' + typer.style(project_name, fg='blue', bold=True))
        typer.echo('Select orm: ' + orm)
        typer.echo('Use dns: ' + dns)
        typer.echo('Use async: ' + async_app)
        typer.echo('Use generic crud: ' + generic_crud)
        if casbin:
            typer.echo('Use rbac: ' + casbin)
        source = github_fs_src if 'True' in dns else gitee_fs_src
        src = get_sqlalchemy_app_src(
            src=source,
            async_app=async_app,
            generic_crud=generic_crud,
            casbin=casbin
        )
        __exec_clone(orm, src, path, path_style)
    else:
        dns = is_dns()
        typer.echo('Project name: ' + typer.style(project_name, fg='blue', bold=True))
        typer.echo('Use orm: ' + orm)
        typer.echo('Use dns: ' + dns)
        src = github_ft_src if 'True' in dns else gitee_ft_src
        __exec_clone(orm, src, path, path_style)


def __exec_clone(orm: str, src: str, path: str, path_style: str) -> None:
    """
    Perform clone.

    :param src:
    :param path:
    :return:
    """
    try:
        if 'sqlalchemy' in orm:
            print(f'⏳ Start cloning branch {src.split()[0]} of repository {src.split()[1]}')
            out = os.system(f'git clone -b {src} {path}')
        else:
            print(f'⏳ Start cloning repository {src}')
            out = os.system(f'git clone {src} {path}')
        if out != 0:
            raise RuntimeError(out)
    except Exception as e:
        print(f'❌ Clone project failed: {e}')
        raise typer.Exit(code=1)
    else:
        print('✅ The project was cloned successfully')
        typer.echo(f'Please go to the directory {path_style} to view')
