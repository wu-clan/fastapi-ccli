#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import keyboard
from prompt_toolkit.output.win32 import (
    NoConsoleScreenBufferError as QuestionaryByTyperCliRunnerError,
)  # noqa
from typer.testing import CliRunner

from fastapi_ccli.cloner.cloner_en import app_en
from fastapi_ccli.cloner.cloner_en_form import app_en_form
from fastapi_ccli.cloner.zh.cloner_zh import app_zh
from fastapi_ccli.cloner.zh.cloner_zh_form import app_zh_form

runner = CliRunner()


def test_cloner_zh():
    """测试非交互模式中文克隆器"""
    result = runner.invoke(app_zh, input="n\n")
    keyboard.send("ctrl+c")
    assert "分析中" in result.stdout
    assert result.exit_code == 1


def test_cloner_zh_ic():
    """测试交互模式中文克隆器"""
    result = runner.invoke(app_zh_form, input="\n \n")
    assert QuestionaryByTyperCliRunnerError
    assert result.exit_code == 1


def test_cloner_en():
    """Test the English cloner in non-interactive mode"""
    result = runner.invoke(app_en, input="n\n")
    keyboard.send("ctrl+c")
    assert "Analyzing" in result.stdout
    assert result.exit_code == 1


def test_cloner_en_ic():
    """Test the English cloner in interactive mode"""
    result = runner.invoke(app_en_form, input="\n \n")
    assert QuestionaryByTyperCliRunnerError
    assert result.exit_code == 1
