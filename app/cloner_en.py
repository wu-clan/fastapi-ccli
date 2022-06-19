#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from typing import Optional

import typer

app_en = typer.Typer()


def orm_callback(orm: str):
    """
    Which to use orm

    :param orm:
    :return:
    """
    if orm:
        if orm == '--s' or orm == '-s':
            use_orm = typer.style('sqlalchemy', fg='blue', bold=True)
        elif orm == '--t' or orm == '-t':
            use_orm = typer.style('tortoise', fg='blue', bold=True)
        else:
            raise typer.BadParameter("Unknown parameter entered, only allowed '--s' / '-s' or '--t' / '-t'")
    else:
        use_orm = typer.style('sqlalchemy', fg='blue', bold=True)
    return use_orm


def is_cdn():
    cdn = typer.confirm('Do you want to use cdn?', default=True)
    if cdn:
        ending = typer.style('True', fg='green', bold=True)
    else:
        ending = typer.style('False', fg='red', bold=True)
    return ending


def is_async_app():
    async_app = typer.confirm('Do you want to use async?', default=True)
    if async_app:
        ending = typer.style('True', fg='green', bold=True)
    else:
        ending = typer.style('False', fg='red', bold=True)
    return ending


def is_generic_crud():
    generic_crud = typer.confirm('Do you want to use generic crud?', default=True)
    if generic_crud:
        ending = typer.style('True', fg='green', bold=True)
    else:
        ending = typer.style('False', fg='red', bold=True)
    return ending


def is_casbin():
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
            help="""
            Which to use orm, if using --s, will use sqlalchemy, the default is to use --s,
            support --s or --t, --s: sqlalchemy; --t: tortoise-orm.
            """
        )
):
    """
    FastAPI project cloner
    """
    if 'sqlalchemy' in orm:
        cdn = is_cdn()
        async_app = is_async_app()
        generic_crud = is_generic_crud()
        casbin = None
        if 'True' in generic_crud:
            casbin = is_casbin()
        typer.echo('Select ORM: ' + orm)
        typer.echo('Use cdn: ' + cdn)
        typer.echo('Use async: ' + async_app)
        typer.echo('Use generics crud: ' + generic_crud)
        if casbin:
            typer.echo('Use rbac: ' + casbin)
        typer.echo('Start cloning project 🚀')
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
            # typer.launch(src)
            os.system(f'git clone {src} ../fastapi_project')
        except Exception as e:
            typer.echo(f'Failed to Clone project ❌: {e}')
            raise typer.Exit(code=1)
        else:
            typer.echo('Clone project succeeded ✅')
            raise typer.Abort()
    else:
        cdn = is_cdn()
        typer.echo('Select ORM: ' + orm)
        typer.echo('Use cdn: ' + cdn)
        typer.echo('Start cloning the project 🚀')
        try:
            if 'True' in cdn:
                src = 'https://github.com/wu-clan/fastapi_tortoise_mysql'
            else:
                src = 'https://gitee.com/wu_cl/fastapi_tortoise_mysql'
            # typer.launch(src)
            os.system(f'git clone {src} ../fastapi_project')
        except Exception as e:
            typer.echo(f'Failed to Clone project ❌: {e}')
            raise typer.Exit(code=1)
        else:
            typer.echo('Clone project succeeded ✅')
            raise typer.Abort()


def __sqlalchemy_app_src(*, host: str, async_app: str, generic_crud: str, casbin: str):
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
