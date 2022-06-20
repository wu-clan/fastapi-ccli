#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re
from typing import Optional

import typer

app_en = typer.Typer()


def orm_callback(orm: str) -> str:
    """
    Which to use orm

    :param orm:
    :return:
    """
    if orm:
        if orm == 's':
            use_orm = typer.style('sqlalchemy', fg='green', bold=True)
        elif orm == 't':
            use_orm = typer.style('tortoise', fg='green', bold=True)
        else:
            raise typer.BadParameter("Enter unknown parameters, only allowed 's' or ‘t'")
    else:
        use_orm = typer.style('sqlalchemy', fg='green', bold=True)
    return use_orm


def project_path_callback(project_path: str) -> str:
    """
    Custom project name

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


def is_cdn() -> str:
    cdn = typer.confirm('Do you want to use cdn?', default=False)
    if cdn:
        ending = typer.style('True', fg='green', bold=True)
    else:
        ending = typer.style('False', fg='red', bold=True)
    return ending


def is_async_app() -> str:
    async_app = typer.confirm('Do you want to use async?', default=True)
    if async_app:
        ending = typer.style('True', fg='green', bold=True)
    else:
        ending = typer.style('False', fg='red', bold=True)
    return ending


def is_generic_crud() -> str:
    generic_crud = typer.confirm('Do you want to use generic crud?', default=True)
    if generic_crud:
        ending = typer.style('True', fg='green', bold=True)
    else:
        ending = typer.style('False', fg='red', bold=True)
    return ending


def is_casbin() -> str:
    casbin = typer.confirm('Do you want to use rbac?', default=True)
    if casbin:
        ending = typer.style('True', fg='green', bold=True)
    else:
        ending = typer.style('False', fg='red', bold=True)
    return ending


@app_en.command()
def clone(
        orm: Optional[str] = typer.Option(
            None,
            "--orm",
            "-o",
            callback=orm_callback,
            help="Which orm to use, if 's' is used, sqlalchemy will be used, 's' is used by default, "
                 "'s' or 't' is supported, explanation, 's': sqlalchemy；'t': tortoise-orm"
        ),
        project_path: Optional[str] = typer.Option(
            None,
            "--project_path",
            "-pp",
            callback=project_path_callback,
            help="The cloned project path, '..fastapi_project' is used by default, supports absolute path"
                 " or relative path, for example, absolute path: 'D:\\git_project\\ttt\\ttt\\req'; "
                 "relative path: '../fastapi_project'"
        ),
):
    """
    FastAPI project cloner
    """
    path_resolve = project_path if not project_path.startswith("..") else os.path.abspath(project_path)
    path = typer.style(path_resolve if not path_resolve.startswith(".") else os.path.abspath(project_path),
                       fg="green", bold=True)
    project_name = re.split(r'/|\'|\\|\\\\', project_path)[-1]
    if 'sqlalchemy' in orm:
        cdn = is_cdn()
        async_app = is_async_app()
        generic_crud = is_generic_crud()
        casbin = None
        if 'True' in generic_crud:
            casbin = is_casbin()
        typer.echo('Start cloning project 🚀')
        typer.echo('Project name: ' + typer.style(project_name, fg='blue', bold=True))
        typer.echo('Select ORM: ' + orm)
        typer.echo('Use cdn: ' + cdn)
        typer.echo('Use async: ' + async_app)
        typer.echo('Use generics crud: ' + generic_crud)
        if casbin:
            typer.echo('使用 rbac: ' + casbin)
        try:
            if 'True' in cdn:
                src = __sqlalchemy_app_src(
                    host='https://github.com/wu-clan/fastapi_sqlalchemy_mysql',
                    async_app=async_app,
                    generic_crud=generic_crud,
                    casbin=casbin
                )
            else:
                src = __sqlalchemy_app_src(
                    host='https://gitee.com/wu_cl/fastapi_sqlalchemy_mysql',
                    async_app=async_app,
                    generic_crud=generic_crud,
                    casbin=casbin
                )
            # typer.echo(src)
            # typer.launch(src)
            os.system(f'git clone {src} {project_name}')
        except Exception as e:
            typer.echo(f'Clone project failed ❌: {e}')
            raise typer.Exit(code=1)
        else:
            typer.echo('The project was cloned successfully ✅')
            typer.echo(f'Please go to the directory {path} to view')
            raise typer.Abort()
    else:
        cdn = is_cdn()
        typer.echo('Start cloning project 🚀')
        typer.echo('Project name: ' + typer.style(project_name, fg='blue', bold=True))
        typer.echo('Select ORM: ' + orm)
        typer.echo('Use cdn: ' + cdn)
        try:
            if 'True' in cdn:
                src = 'https://github.com/wu-clan/fastapi_tortoise_mysql'
            else:
                src = 'https://gitee.com/wu_cl/fastapi_tortoise_mysql'
            # typer.echo(src)
            # typer.launch(src)
            os.system(f'git clone {src} {project_name}')
        except Exception as e:
            typer.echo(f'Clone project failed ❌: {e}')
            raise typer.Exit(code=1)
        else:
            typer.echo('The project was cloned successfully ✅')
            typer.echo(f'Please go to the directory {path} to view')
            raise typer.Abort()


def __sqlalchemy_app_src(*, host: str, async_app: str, generic_crud: str, casbin: str) -> str:
    """
    sqlalchemy app download address resolution.

    :param host:
    :param async_app:
    :param generic_crud:
    :param casbin:
    :return:
    """
    if 'True' in async_app:
        tree = ['', '/tree/async-CRUDBase', '/tree/async-Plus']
        if 'True' in generic_crud:
            generic = [tree[1], tree[2]]
            if 'True' in casbin:
                rbac = generic[1]
                end = host + rbac
            else:
                rbac = generic[0]
                end = host + rbac
        else:
            generic = tree[0]
            end = host + generic
        clone_src = end
    else:
        tree = ['/tree/sync', '/tree/sync-CRUDBase', '/tree/sync-Plus']
        if 'True' in generic_crud:
            generic = [tree[1], tree[2]]
            if 'True' in casbin:
                rbac = generic[1]
                end = host + rbac
            else:
                rbac = generic[0]
                end = host + rbac
        else:
            generic = tree[0]
            end = host + generic
        clone_src = end
    return clone_src
