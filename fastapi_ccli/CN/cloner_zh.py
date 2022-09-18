#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re
import time
from typing import Optional
from rich import print

import typer

from fastapi_ccli import GREEN, RED, github_fs_src, gitee_fs_src, github_ft_src, gitee_ft_src
from fastapi_ccli.utils.get_country import get_current_country
from fastapi_ccli.utils.get_ip import get_net_ip
from fastapi_ccli.utils.get_path import get_project_path
from fastapi_ccli.utils.get_src import get_sqlalchemy_app_src

app_zh = typer.Typer(rich_markup_mode="rich")


def orm_callback(orm: str) -> str:
    """
    使用哪个 orm

    :param orm:
    :return:
    """
    if orm:
        if orm == 'sqlalchemy' or orm == 's':
            use_orm = typer.style('sqlalchemy', fg='green', bold=True)
        elif orm == 'tortoise-orm' or orm == 't':
            use_orm = typer.style('tortoise-orm', fg='green', bold=True)
        else:
            raise typer.BadParameter("输入未知参数，只允许 'sqlalchemy' / 's' or 'tortoise-orm' / 't'")
    else:
        use_orm = typer.style('sqlalchemy', fg='green', bold=True)
    return use_orm


def project_path_callback(project_path: str) -> str:
    """
    自定义项目路径

    :param project_path:
    :return:
    """
    if project_path:
        if not isinstance(project_path, str):
            raise typer.BadParameter("输入错误参数，请输入正确的路径'")
        else:
            use_project_name = project_path
    else:
        use_project_name = '../fastapi_project'
    return use_project_name


def is_dns() -> str:
    dns = typer.confirm('你想使用 dns 吗?', default=False)
    with typer.progressbar(range(5), label='分析中') as progress:
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
            if dns:
                ending = GREEN
            else:
                ending = RED
        else:
            if dns:
                ending = RED
            else:
                ending = GREEN
        return ending


def is_async_app() -> str:
    async_app = typer.confirm('你想使用异步吗?', default=True)
    if async_app:
        ending = GREEN
    else:
        ending = RED
    return ending


def is_generic_crud() -> str:
    generic_crud = typer.confirm('你想使用泛型 crud 吗?', default=True)
    if generic_crud:
        ending = GREEN
    else:
        ending = RED
    return ending


def is_casbin() -> str:
    casbin = typer.confirm('你想使用 rbac 吗?', default=True)
    if casbin:
        ending = GREEN
    else:
        ending = RED
    return ending


@app_zh.command(epilog="由 :beating_heart: wu-clan 制作")
def cloner(
        orm: Optional[str] = typer.Option(
            None,
            "--orm",
            "-o",
            callback=orm_callback,
            help="选择要使用的 orm，默认为 sqlalchemy，支持 sqlalchemy 或 tortoise-orm，也可以使用简写，s 或 t。"
        ),
        project_path: Optional[str] = typer.Option(
            None,
            "--path",
            "-p",
            callback=project_path_callback,
            help="项目克隆路径，默认为 ../fastapi_project，支持绝对路径或相对路径，举例，"
                 "绝对路径：D:\\fastapi_project，相对路径：../fastapi_project。"
        ),
):
    """
    FastAPI 项目克隆器
    """
    path = get_project_path(project_path)
    path_style = typer.style(path, fg='green', bold=True)
    project_name = typer.style(re.split(r'/|\'|\\|\\\\', project_path)[-1], fg='blue', bold=True)
    if 'sqlalchemy' in orm:
        dns = is_dns()
        async_app = is_async_app()
        generic_crud = is_generic_crud()
        casbin = None
        if 'True' in generic_crud:
            casbin = is_casbin()
        typer.echo('项目名称：' + project_name)
        print('选择 ORM：' + orm)
        typer.echo('使用 dns：' + dns)
        typer.echo('使用异步：' + async_app)
        typer.echo('使用泛型 crud：' + generic_crud)
        if casbin:
            typer.echo('使用 rbac：' + casbin)
        if 'True' in dns:
            src = get_sqlalchemy_app_src(
                src=github_fs_src,
                async_app=async_app,
                generic_crud=generic_crud,
                casbin=casbin
            )
        else:
            src = get_sqlalchemy_app_src(
                src=gitee_fs_src,
                async_app=async_app,
                generic_crud=generic_crud,
                casbin=casbin
            )
        __exec_clone(orm, src, path, path_style)
    else:
        dns = is_dns()
        typer.echo('项目名称：' + project_name)
        print('选择 ORM：' + orm)
        typer.echo('使用 dns：' + dns)
        if 'True' in dns:
            src = github_ft_src
        else:
            src = gitee_ft_src
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
        if 'sqlalchemy' in orm:
            print(f'⏳ 开始克隆存储库 {src.split()[1]} 的 {src.split()[0]} 分支')
            out = os.system(f'git clone -b {src} {path}')
        else:
            print(f'⏳ 开始克隆存储库 {src}')
            out = os.system(f'git clone {src} {path}')
        if out != 0:
            raise RuntimeError(out)
    except Exception as e:
        print(f'❌ 克隆项目失败: {e}')
        raise typer.Exit(code=1)
    else:
        print('✅ 项目克隆成功')
        typer.echo(f'请到目录 {path_style} 查看')
        raise typer.Abort()
