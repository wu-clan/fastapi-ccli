#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re
import time
from typing import Optional

import questionary
import typer
from rich import print

from fastapi_ccli import GREEN, RED, github_fs_src, gitee_fs_src, github_ft_src, gitee_ft_src
from fastapi_ccli.utils.get_country import get_current_country
from fastapi_ccli.utils.get_ip import get_net_ip
from fastapi_ccli.utils.get_path import get_project_path
from fastapi_ccli.utils.get_src import get_sqlalchemy_app_src

app_en_form = typer.Typer(rich_markup_mode="rich")


def project_path_callback(project_path: str) -> str:
    """
    Select project path...

    :param project_path:
    :return:
    """
    if project_path:
        if not isinstance(project_path, str):
            raise typer.BadParameter("Bad input parameter, please enter the correct path")
        else:
            use_project_name = project_path
    else:
        use_project_name = '../fastapi_project'
    return use_project_name


def orm_style(orm: str) -> str:
    """
    orm stylization...

    :param orm:
    :return:
    """
    return typer.style(orm, fg='green', bold=True)


def is_dns(dns: bool) -> str:
    """
    Whether to use dns...

    :param dns:
    :return:
    """
    with typer.progressbar(range(5), label='  Analyzing') as progress:
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
            ending = GREEN if 'Yes' in dns else RED
        else:
            ending = RED if 'Yes' in dns else GREEN
        return ending


def is_async_app(async_app: bool) -> str:
    """
    Whether to use async...

    :param async_app:
    :return:
    """
    ending = GREEN if 'Yes' in async_app else RED
    return ending


def is_generic_crud(generic_crud: bool) -> str:
    """
    Whether to use generic crud...

    :param generic_crud:
    :return:
    """
    ending = GREEN if 'Yes' in generic_crud else RED
    return ending


def is_casbin(casbin: bool) -> str:
    """
    Whether to use rbac...

    :param casbin:
    :return:
    """
    ending = GREEN if 'Yes' in casbin else RED
    return ending


@app_en_form.command(epilog="Made by :beating_heart: wu-clan")
def cloner(
        _version: Optional[bool] = typer.Option(
            None,
            "--version",
            '-V',
            help="Print version information and quit"
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
    project_name = typer.style(re.split(r'/|\'|\\|\\\\', project_path)[-1], fg='blue', bold=True)
    result_if = questionary.form(
        orm=questionary.select('Please select the orm you want to use:', choices=['SQLAlchemy', 'Tortoise-ORM'],
                               default='SQLAlchemy'),
        dns=questionary.select('Do you want to use dns?', choices=['Yes', 'No'], default='No'),
    ).ask()
    if len(result_if) == 0:
        raise typer.Abort
    dns = is_dns(result_if['dns'])
    orm = orm_style(result_if['orm'])
    if 'SQLAlchemy' in orm:
        result = questionary.form(
            async_app=questionary.select('Do you want to use async?', choices=['Yes', 'No']),
            generic_crud=questionary.select('Do you want to use generic crud?', choices=['Yes', 'No']),
        ).ask()
        if len(result) == 0:
            raise typer.Abort
        async_app = is_async_app(result['async_app'])
        generic_crud = is_generic_crud(result['generic_crud'])
        casbin = None
        if 'True' in generic_crud:
            rbac = questionary.form(
                casbin=questionary.select('Do you want to use rbac authentication?', choices=['Yes', 'No'])
            ).ask()
            if len(rbac) == 0:
                raise typer.Abort
            if rbac['casbin'] == 'Yes':
                casbin = is_casbin(rbac['casbin'])
        typer.echo('Project name：' + project_name)
        typer.echo('Use orm：' + orm)
        typer.echo('Use dns：' + dns)
        typer.echo('Use async：' + async_app)
        typer.echo('Use generic crud：' + generic_crud)
        if casbin:
            typer.echo('Use rbac authentication：' + casbin)
        source = github_fs_src if 'True' in dns else gitee_fs_src
        src = get_sqlalchemy_app_src(
            src=source,
            async_app=async_app,
            generic_crud=generic_crud,
            casbin=casbin
        )
        __exec_clone(orm, src, path, path_style)
    else:
        typer.echo('Project name：' + project_name)
        typer.echo('Use orm：' + orm)
        typer.echo('Use dns：' + dns)
        src = github_ft_src if 'True' in dns else gitee_ft_src
        __exec_clone(orm, src, path, path_style)


def __exec_clone(orm: str, src: str, path: str, path_style: str) -> None:
    """
    Perform clone.

    :param orm:
    :param src:
    :param path:
    :return:
    """
    try:
        # typer.launch(src)
        if 'SQLAlchemy' in orm:
            print(f'⏳ Start cloning the {src.split()[0]} branch of the repository {src.split()[1]}')
            out = os.system(f'git clone -b {src} {path}')
        else:
            print(f'⏳ Start cloning the repository {src}')
            out = os.system(f'git clone {src} {path}')
        if out != 0:
            raise RuntimeError(out)
    except Exception as e:
        print(f'❌ Clone repository failed: {e}')
        raise typer.Exit(code=1)
    else:
        print('✅ The repository was cloned successfully')
        typer.echo(f'Please go to the directory {path_style} to view')
