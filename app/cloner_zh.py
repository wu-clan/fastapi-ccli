#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from typing import Optional

import typer

app_zh = typer.Typer()


def orm_callback(orm: str):
    """
    使用哪个 orm

    :param orm:
    :return:
    """
    if orm:
        if orm == '--s' or orm == '-s':
            use_orm = typer.style('sqlalchemy', fg='blue', bold=True)
        elif orm == '--t' or orm == '-t':
            use_orm = typer.style('tortoise', fg='blue', bold=True)
        else:
            raise typer.BadParameter("输入未知参数，只允许 '--s' / '-s' or '--t' / '-t'")
    else:
        use_orm = typer.style('sqlalchemy', fg='blue', bold=True)
    return use_orm


def is_cdn():
    cdn = typer.confirm('你想使用 cdn 吗?', default=False)
    if cdn:
        ending = typer.style('True', fg='green', bold=True)
    else:
        ending = typer.style('False', fg='red', bold=True)
    return ending


def is_async_app():
    async_app = typer.confirm('你想使用异步吗?', default=True)
    if async_app:
        ending = typer.style('True', fg='green', bold=True)
    else:
        ending = typer.style('False', fg='red', bold=True)
    return ending


def is_generic_crud():
    generic_crud = typer.confirm('你想使用泛型 crud 吗?', default=True)
    if generic_crud:
        ending = typer.style('True', fg='green', bold=True)
    else:
        ending = typer.style('False', fg='red', bold=True)
    return ending


def is_casbin():
    casbin = typer.confirm('你想使用 rbac 吗?', default=True)
    if casbin:
        ending = typer.style('True', fg='green', bold=True)
    else:
        ending = typer.style('False', fg='red', bold=True)
    return ending


@app_zh.command()
def clone(
        orm: Optional[str] = typer.Option(
            None,
            "--orm",
            "-o",
            callback=orm_callback,
            help="""
            使用哪个 orm, 如果使用 --s, 则会使用 sqlalchemy, 默认使用的是 --s,
            支持 --s 或 --t, --s: sqlalchemy; --t: tortoise-orm.
            """
        )
):
    """
    FastAPI 项目克隆器
    """
    if 'sqlalchemy' in orm:
        cdn = is_cdn()
        async_app = is_async_app()
        generic_crud = is_generic_crud()
        casbin = None
        if 'True' in generic_crud:
            casbin = is_casbin()
        typer.echo('选择 ORM: ' + orm)
        typer.echo('使用 cdn: ' + cdn)
        typer.echo('使用异步: ' + async_app)
        typer.echo('使用泛型 crud: ' + generic_crud)
        if casbin:
            typer.echo('使用 rbac: ' + casbin)
        typer.echo('开始克隆项目 🚀')
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
            typer.echo(f'克隆项目失败 ❌: {e}')
            raise typer.Exit(code=1)
        else:
            typer.echo('克隆项目成功 ✅')
            raise typer.Abort()
    else:
        cdn = is_cdn()
        typer.echo('选择 ORM: ' + orm)
        typer.echo('使用 cdn: ' + cdn)
        typer.echo('开始克隆项目 🚀')
        try:
            if 'True' in cdn:
                src = 'https://github.com/wu-clan/fastapi_tortoise_mysql'
            else:
                src = 'https://gitee.com/wu_cl/fastapi_tortoise_mysql'
            # typer.launch(src)
            os.system(f'git clone {src} ../fastapi_project')
        except Exception as e:
            typer.echo(f'克隆项目失败 ❌: {e}')
            raise typer.Exit(code=1)
        else:
            typer.echo('克隆项目成功 ✅')
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
