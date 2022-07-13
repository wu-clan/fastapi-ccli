#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import typer
from prompt_toolkit.output.win32 import NoConsoleScreenBufferError as QuestionaryByTyperCliRunnerError
from typer.testing import CliRunner

from fastapi_ccli.main import main

app = typer.Typer()
app.command()(main)

runner = CliRunner()


def test_cloner_zh():
    """ 测试非交互模式中文克隆器 """
    result = runner.invoke(app, input='y\n n\n n\n')
    typer.Abort()
    assert '分析中' in result.stdout
    assert result.exit_code == 1


def test_cloner_zh_ic():
    """ 测试交互模式中文克隆器 """
    result = runner.invoke(app, input='y\n y\n \n \n')
    assert QuestionaryByTyperCliRunnerError
    assert result.exit_code == 1


def test_cloner_en():
    """ Test the English cloner in non-interactive mode """
    result = runner.invoke(app, input='n\n n\n n\n')
    typer.Abort()
    assert 'Analyzing' in result.stdout
    assert result.exit_code == 1


def test_cloner_en_ic():
    """ Test the English cloner in interactive mode """
    result = runner.invoke(app, input='n\n y\n \n \n')
    assert QuestionaryByTyperCliRunnerError
    assert result.exit_code == 1
