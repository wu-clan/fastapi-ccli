#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re
import time
from typing import Optional

import typer

from app import GREEN, RED
from app.utils.get_country import get_current_country
from app.utils.get_ip import get_net_ip
from app.utils.get_path import get_project_path
from app.utils.get_src import get_sqlalchemy_app_src

app_en = typer.Typer()


def orm_callback(orm: str) -> str:
    """
    Which to use orm

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
                "Enter unknown parameters, only allowed 'sqlalchemy' / 's' or 'tortoise-orm' / 't'")
    else:
        use_orm = typer.style('sqlalchemy', fg='green', bold=True)
    return use_orm


def project_path_callback(project_path: str) -> str:
    """
    custom project path

    :param project_path:
    :return:
    """
    if project_path:
        if not isinstance(project_path, str):
            raise typer.BadParameter("Wrong parameter input, Only strings are allowed'")
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
            if len(ip) > 0:
                rp = get_current_country(ip)
                if 'CN' in rp:
                    if dns:
                        ending = GREEN
                    else:
                        ending = RED
                else:
                    if dns:
                        ending = RED
                    else:
                        ending = GREEN
                # Visual effects
                time.sleep(0.3)
                progress.update(5)
                break
            else:
                time.sleep(0.3)
                progress.update(i)
            # If no ip, then it uses GitHub, this is temporary solution.
            ending = RED
    return ending


def is_async_app() -> str:
    async_app = typer.confirm('Do you want to use async?', default=True)
    if async_app:
        ending = GREEN
    else:
        ending = RED
    return ending


def is_generic_crud() -> str:
    generic_crud = typer.confirm('Do you want to use generic crud?', default=True)
    if generic_crud:
        ending = GREEN
    else:
        ending = RED
    return ending


def is_casbin() -> str:
    casbin = typer.confirm('Do you want to use rbac?', default=True)
    if casbin:
        ending = GREEN
    else:
        ending = RED
    return ending


@app_en.command()
def clone(
        orm: Optional[str] = typer.Option(
            None,
            "--orm",
            "-o",
            callback=orm_callback,
            help="""
            Which orm to use, sqlalchemy is used by default, sqlalchemy or tortoise-orm is supported, description, 
            shorthand can be used, s == sqlalchemy, t == tortoise-orm
            """
        ),
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
    project_name = re.split(r'/|\'|\\|\\\\', project_path)[-1]
    if 'sqlalchemy' in orm:
        dns = is_dns()
        async_app = is_async_app()
        generic_crud = is_generic_crud()
        casbin = None
        if 'True' in generic_crud:
            casbin = is_casbin()
        typer.echo('Project name: ' + typer.style(project_name, fg='blue', bold=True))
        typer.echo('Select ORM: ' + orm)
        typer.echo('Use dns: ' + dns)
        typer.echo('Use async: ' + async_app)
        typer.echo('Use generics crud: ' + generic_crud)
        if casbin:
            typer.echo('Use rbac: ' + casbin)
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
        dns = is_dns()
        typer.echo('Project name: ' + typer.style(project_name, fg='blue', bold=True))
        typer.echo('Select ORM: ' + orm)
        typer.echo('Use dns: ' + dns)
        if 'True' in dns:
            src = 'https://github.com/wu-clan/fastapi_tortoise_mysql.git'
        else:
            src = 'https://gitee.com/wu_cl/fastapi_tortoise_mysql.git'
        __exec_clone(orm, src, path, path_style)


def __exec_clone(orm: str, src: str, path: str, path_style: str) -> None:
    """
    Perform clone

    :param src:
    :param path:
    :return:
    """
    try:
        # typer.launch(src)
        if 'sqlalchemy' in orm:
            typer.echo(f'Start cloning branch {src.split()[0]} of repository {src.split()[1]} 🚀')
            out = os.system(f'git clone -b {src} {path}')
        else:
            typer.echo(f'Start cloning repository {src} 🚀')
            out = os.system(f'git clone {src} {path}')
        if out != 0:
            raise RuntimeError(out)
    except Exception as e:
        typer.echo(f'Clone project failed ❌: {e}')
        raise typer.Exit(code=1)
    else:
        typer.echo('The project was cloned successfully ✅')
        typer.echo(f'Please go to the directory {path_style} to view')
        raise typer.Abort()
