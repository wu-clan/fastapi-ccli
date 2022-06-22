#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re
import time
from typing import Optional

import questionary
import typer

from app import GREEN, RED
from app.utils.get_country import get_current_country
from app.utils.get_ip import get_net_ip
from app.utils.get_path import get_project_path
from app.utils.get_src import get_sqlalchemy_app_src

app_en_ic = typer.Typer()


def project_path_callback(project_path: str) -> str:
    """
    Custom project path

    :param project_path:
    :return:
    """
    if project_path:
        if not isinstance(project_path, str):
            raise typer.BadParameter("Bad input parameter, only strings are allowed'")
        else:
            use_project_name = project_path
    else:
        use_project_name = '../fastapi_project'
    return use_project_name


def orm_style(orm: str) -> str:
    """
    orm stylization

    :param orm:
    :return:
    """
    return typer.style(orm, fg='green', bold=True)


def is_dns(dns: bool) -> str:
    """
    Whether to use dns

    :param dns:
    :return:
    """
    with typer.progressbar(range(5), label='  Analyzing') as progress:
        for i in progress:
            ip = get_net_ip()
            if ip:
                # Visual effects
                time.sleep(0.3)
                progress.update(5)
                break
            else:
                time.sleep(0.3)
                progress.update(i)
                continue
        rp = get_current_country(ip)
        if 'CN' in rp:
            if 'Yes' in dns:
                ending = GREEN
            else:
                ending = RED
        else:
            if 'Yes' in dns:
                ending = RED
            else:
                ending = GREEN
        return ending


def is_async_app(async_app: bool) -> str:
    """
    Whether to use async

    :param async_app:
    :return:
    """
    if 'Yes' in async_app:
        ending = GREEN
    else:
        ending = RED
    return ending


def is_generic_crud(generic_crud: bool) -> str:
    """
    Whether to use generic crud

    :param generic_crud:
    :return:
    """
    if 'Yes' in generic_crud:
        ending = GREEN
    else:
        ending = RED
    return ending


def is_casbin(casbin: bool) -> str:
    """
    Whether to use rbac

    :param casbin:
    :return:
    """
    if 'Yes' in casbin:
        ending = GREEN
    else:
        ending = RED
    return ending


@app_en_ic.command()
def clone(
        project_path: Optional[str] = typer.Option(
            None,
            "--project_path",
            "-pp",
            callback=project_path_callback,
            help="""
            The cloned project path, using ../fastapi_project by default, supports absolute path or relative path, 
            for example, Absolute path: D:\\fastapi project, relative path: ../fastapi project
            """
        ),
):
    """
    FastAPI project cloner
    """
    path = get_project_path(project_path)
    path_style = typer.style(path, fg='green', bold=True)
    project_name = typer.style(re.split(r'/|\'|\\|\\\\', project_path)[-1], fg='blue', bold=True)
    result_if = questionary.form(
        orm=questionary.select('Please select the orm you want to use:', choices=['SQLAlchemy', 'Tortoise-ORM']),
        dns=questionary.select('Do you want to use dns?', choices=['Yes', 'No']),
    ).unsafe_ask()
    dns = is_dns(result_if['dns'])
    orm = orm_style(result_if['orm'])
    if 'SQLAlchemy' in orm:
        result = questionary.form(
            async_app=questionary.select('Do you want to use async?', choices=['Yes', 'No']),
            generic_crud=questionary.select('Do you want to use generic crud?', choices=['Yes', 'No']),
            casbin=questionary.select('Do you want to use rbac?', choices=['Yes', 'No']),
        ).unsafe_ask()
        async_app = is_async_app(result['async_app'])
        generic_crud = is_generic_crud(result['generic_crud'])
        casbin = None
        if 'True' in generic_crud:
            casbin = is_casbin(result['casbin'])
        typer.echo('Project name：' + project_name)
        typer.echo('Use orm：' + orm)
        typer.echo('Use dns：' + dns)
        typer.echo('Use async：' + async_app)
        typer.echo('Use generics crud：' + generic_crud)
        if casbin:
            typer.echo('Use rbac：' + casbin)
        if 'True' in dns:
            src = get_sqlalchemy_app_src(
                src='https://github.com/wu-clan/fastapi_sqlalchemy_mysql.git',
                async_app=async_app,
                generic_crud=generic_crud,
                casbin=casbin
            )
        else:
            src = get_sqlalchemy_app_src(
                src='https://gitee.com/wu_cl/fastapi_sqlalchemy_mysql.git',
                async_app=async_app,
                generic_crud=generic_crud,
                casbin=casbin
            )
        __exec_clone(orm, src, path, path_style)
    else:
        typer.echo('Project name：' + project_name)
        typer.echo('Use orm：' + orm)
        typer.echo('Use dns：' + dns)
        if 'True' in dns:
            src = 'https://github.com/wu-clan/fastapi_tortoise_mysql.git'
        else:
            src = 'https://gitee.com/wu_cl/fastapi_tortoise_mysql.git'
        __exec_clone(orm, src, path, path_style)


def __exec_clone(orm: str, src: str, path: str, path_style: str) -> None:
    """
    执行克隆

    :param orm:
    :param src:
    :param path:
    :return:
    """
    try:
        # typer.launch(src)
        if 'SQLAlchemy' in orm:
            typer.echo(f'Start cloning the {src.split()[0]} branch of the repository {src.split()[1]} 🚀')
            out = os.system(f'git clone -b {src} {path}')
        else:
            typer.echo(f'Start cloning the repository {src} 🚀')
            out = os.system(f'git clone {src} {path}')
        if out != 0:
            raise RuntimeError(out)
    except Exception as e:
        typer.echo(f'Clone repository failed ❌: {e}')
        raise typer.Exit(code=1)
    else:
        typer.echo('The repository was cloned successfully ✅')
        typer.echo(f'Please go to the directory {path_style} to view')
        raise typer.Abort()
