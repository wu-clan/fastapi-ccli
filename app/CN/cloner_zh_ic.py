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

app_zh_ic = typer.Typer()


def project_path_callback(project_path: str) -> str:
    """
    自定义项目路径

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


def orm_style(orm: str) -> str:
    """
    orm 风格

    :param orm:
    :return:
    """
    return typer.style(orm, fg='green', bold=True)


def is_dns(dns: str) -> str:
    """
    是否使用 dns

    :param dns:
    :return:
    """
    with typer.progressbar(range(5), label='  分析中') as progress:
        for i in progress:
            ip = get_net_ip()
            if ip:
                # 视觉效果
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


def is_async_app(async_app: str) -> str:
    """
    是否使用 async

    :param async_app:
    :return:
    """
    if 'Yes' in async_app:
        ending = GREEN
    else:
        ending = RED
    return ending


def is_generic_crud(generic_crud: str) -> str:
    """
    是否使用泛型

    :param generic_crud:
    :return:
    """
    if 'Yes' in generic_crud:
        ending = GREEN
    else:
        ending = RED
    return ending


def is_casbin(casbin: str) -> str:
    """
    是否使用 rbac

    :param casbin:
    :return:
    """
    if 'Yes' in casbin:
        ending = GREEN
    else:
        ending = RED
    return ending


@app_zh_ic.command()
def clone(
        project_path: Optional[str] = typer.Option(
            None,
            "--project_path",
            "-pp",
            callback=project_path_callback,
            help="""
            克隆后的项目路径，默认使用 ../fastapi_project，支持绝对路径或相对路径，举例，
            绝对路径：D:\\fastapi_project，相对路径：../fastapi_project
            """
        ),
):
    """
    FastAPI 项目克隆器
    """
    path = get_project_path(project_path)
    path_style = typer.style(path, fg='green', bold=True)
    project_name = typer.style(re.split(r'/|\'|\\|\\\\', project_path)[-1], fg='blue', bold=True)
    result_if = questionary.form(
        orm=questionary.select('请选择你要使用的 orm', choices=['SQLAlchemy', 'Tortoise-ORM']),
        dns=questionary.select('你想使用 dns 吗？', choices=['Yes', 'No']),
    ).unsafe_ask()
    dns = is_dns(result_if['dns'])
    orm = orm_style(result_if['orm'])
    if 'SQLAlchemy' in orm:
        result = questionary.form(
            async_app=questionary.select('你想使用异步吗？', choices=['Yes', 'No']),
            generic_crud=questionary.select('你想使用泛型 crud 吗？', choices=['Yes', 'No']),
            casbin=questionary.select('你想使用 rbac 吗？', choices=['Yes', 'No']),
        ).unsafe_ask()
        async_app = is_async_app(result['async_app'])
        generic_crud = is_generic_crud(result['generic_crud'])
        casbin = None
        if 'True' in generic_crud:
            casbin = is_casbin(result['casbin'])
        typer.echo('项目名称：' + project_name)
        typer.echo('选择 ORM：' + orm)
        typer.echo('使用 DNS：' + dns)
        typer.echo('使用异步：' + async_app)
        typer.echo('使用泛型 CRUD：' + generic_crud)
        if casbin:
            typer.echo('使用 RBAC：' + casbin)
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
        typer.echo('项目名称：' + project_name)
        typer.echo('选择 ORM：' + orm)
        typer.echo('使用 DNS：' + dns)
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
            typer.echo(f'开始克隆存储库 {src.split()[1]} 的 {src.split()[0]} 分支 🚀')
            out = os.system(f'git clone -b {src} {path}')
        else:
            typer.echo(f'开始克隆存储库 {src} 🚀')
            out = os.system(f'git clone {src} {path}')
        if out != 0:
            raise RuntimeError(out)
    except Exception as e:
        typer.echo(f'克隆项目失败 ❌: {e}')
        raise typer.Exit(code=1)
    else:
        typer.echo('项目克隆成功 ✅')
        typer.echo(f'请到目录 {path_style} 查看')
        raise typer.Abort()
