#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re
from typing import Optional

import typer

app_zh = typer.Typer()


def orm_callback(orm: str) -> str:
    """
    使用哪个 orm

    :param orm:
    :return:
    """
    if orm:
        if orm == 's':
            use_orm = typer.style('sqlalchemy', fg='green', bold=True)
        elif orm == 't':
            use_orm = typer.style('tortoise', fg='green', bold=True)
        else:
            raise typer.BadParameter("输入未知参数，只允许 's' or ‘t'")
    else:
        use_orm = typer.style('sqlalchemy', fg='green', bold=True)
    return use_orm


def project_path_callback(project_path: str) -> str:
    """
    自定义项目名

    :param project_path:
    :return:
    """
    if project_path:
        if not isinstance(project_path, str):
            raise typer.BadParameter("输入错误参数，只允许字符串'")
        else:
            use_project_name = project_path
    else:
        use_project_name = '../fastapi_project'
    return use_project_name


def is_cdn() -> str:
    cdn = typer.confirm('你想使用 cdn 吗?', default=False)
    if cdn:
        ending = typer.style('True', fg='green', bold=True)
    else:
        ending = typer.style('False', fg='red', bold=True)
    return ending


def is_async_app() -> str:
    async_app = typer.confirm('你想使用异步吗?', default=True)
    if async_app:
        ending = typer.style('True', fg='green', bold=True)
    else:
        ending = typer.style('False', fg='red', bold=True)
    return ending


def is_generic_crud() -> str:
    generic_crud = typer.confirm('你想使用泛型 crud 吗?', default=True)
    if generic_crud:
        ending = typer.style('True', fg='green', bold=True)
    else:
        ending = typer.style('False', fg='red', bold=True)
    return ending


def is_casbin() -> str:
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
            help="使用哪个 orm，如果使用 s，则会使用 sqlalchemy，默认使用的是 s，支持 s 或 t，"
                 "说明，s：sqlalchemy；t：tortoise-orm"
        ),
        project_path: Optional[str] = typer.Option(
            None,
            "--project_path",
            "-pp",
            callback=project_path_callback,
            help="克隆后的项目路径，默认使用 ../fastapi_project，默认克隆路径为当前路径，支持绝对路径或相对路径，"
                 "举例，绝对路径：D:\\git_project\\ttt\\ttt\\req；相对路径：../fastapi_project"
        ),
):
    """
    FastAPI 项目克隆器
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
        typer.echo('开始克隆项目 🚀')
        typer.echo('项目名称：' + typer.style(project_name, fg='blue', bold=True))
        typer.echo('选择 ORM：' + orm)
        typer.echo('使用 cdn：' + cdn)
        typer.echo('使用异步：' + async_app)
        typer.echo('使用泛型 crud：' + generic_crud)
        if casbin:
            typer.echo('使用 rbac：' + casbin)
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
            typer.echo(f'克隆项目失败 ❌：{e}')
            raise typer.Exit(code=1)
        else:
            typer.echo('项目克隆成功 ✅')
            typer.echo(f'请到目录 {path} 查看')
            raise typer.Abort()
    else:
        cdn = is_cdn()
        typer.echo('开始克隆项目 🚀')
        typer.echo('项目名称：' + typer.style(project_name, fg='blue', bold=True))
        typer.echo('选择 ORM：' + orm)
        typer.echo('使用 cdn：' + cdn)
        try:
            if 'True' in cdn:
                src = 'https://github.com/wu-clan/fastapi_tortoise_mysql'
            else:
                src = 'https://gitee.com/wu_cl/fastapi_tortoise_mysql'
            # typer.echo(src)
            # typer.launch(src)
            os.system(f'git clone {src} {project_name}')
        except Exception as e:
            typer.echo(f'克隆项目失败 ❌: {e}')
            raise typer.Exit(code=1)
        else:
            typer.echo('项目克隆成功 ✅')
            typer.echo(f'请到目录 {path} 查看')
            raise typer.Abort()


def __sqlalchemy_app_src(*, host: str, async_app: str, generic_crud: str, casbin: str) -> str:
    """
    sqlalchemy app下载地址解析.

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
