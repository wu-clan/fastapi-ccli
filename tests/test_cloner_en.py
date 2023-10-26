#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pytest
from click import BadParameter, BadOptionUsage
from typer.testing import CliRunner

from fastapi_ccli.cloner.cloner_en import app_en

runner = CliRunner()


def test_en_version():
    """
    test cloner en version
    """
    result = runner.invoke(app_en, ["--version"])
    assert "FastAPI CCLI" in result.output
    assert result.exit_code == 0
    result = runner.invoke(app_en, ["-V"])
    assert "FastAPI CCLI" in result.output
    assert result.exit_code == 0


def test_en_orm_sqlalchemy():
    """
    test cloner en orm sqlalchemy
    """
    result = runner.invoke(app_en, ["--orm", "sqlalchemy"])
    assert result.output == ""
    assert result.exit_code == 0


def test_en_orm_tortoise():
    """
    test cloner en orm tortoise
    """
    result = runner.invoke(app_en, ["--orm", "tortoise"])
    assert result.output == ""
    assert result.exit_code == 0


def test_en_orm_sqlmodel():
    """
    test cloner en orm sqlmodel
    """
    result = runner.invoke(app_en, ["--orm", "sqlmodel"])
    assert result.output == ""
    assert result.exit_code == 0


@pytest.mark.skip("Unknown reasons, invoke was unable to catch the exception")
def test_en_orm_illegal_value():
    """
    test cloner en orm illegal value
    """
    with pytest.raises(BadParameter) as exc_info:
        runner.invoke(app_en, ["--orm", "none"], catch_exceptions=False)
    assert exc_info.value.exit_code == 2
    assert (
        exc_info.value.message
        == "Invalid value: Enter unknown parameters, only allowed 'sqlalchemy' / 'tortoise' / 'sqlmodel'"
    )


@pytest.mark.skip("Unknown reasons, invoke was unable to catch the exception")
def test_en_orm_no_argument():
    """
    test cloner en orm no argument
    """
    with pytest.raises(BadOptionUsage) as exc_info:
        runner.invoke(app_en, ["--orm"], catch_exceptions=False)
    assert exc_info.value.exit_code == 2
    assert exc_info.value.message == "Option '--orm' requires an argument."


@pytest.mark.skip("Unknown reasons, invoke was unable to catch the exception")
def test_en_project_path():
    """
    test cloner en project path
    """
    with pytest.raises(BadParameter) as exc_info:
        runner.invoke(app_en, ["--path", "100"], catch_exceptions=False)
    assert exc_info.value.exit_code == 2
    assert exc_info.value.message == "Invalid value: Wrong parameter input, please enter the correct path"
