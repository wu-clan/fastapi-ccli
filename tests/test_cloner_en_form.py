#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pytest

from click import BadParameter
from typer.testing import CliRunner

from fastapi_ccli.cloner.cloner_en_form import app_en_form

runner = CliRunner()


def test_en_form_version():
    """
    test cloner en form version
    """
    result = runner.invoke(app_en_form, ['--version'])
    assert 'FastAPI CCLI' in result.output
    assert result.exit_code == 0
    result = runner.invoke(app_en_form, ['-V'])
    assert 'FastAPI CCLI' in result.output
    assert result.exit_code == 0


@pytest.mark.skip('Unknown reasons, invoke was unable to catch the exception')
def test_en_form_orm():
    """
    test cloner en form orm
    """
    with pytest.raises(BadParameter) as exc_info:
        runner.invoke(app_en_form, ['--path', '100'], catch_exceptions=False)
    assert exc_info.value.exit_code == 2
    assert exc_info.value.message == 'Invalid value: Wrong parameter input, please enter the correct path'
