#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys

import questionary
import typer

from fastapi_ccli.cloner.cloner_en import app_en
from fastapi_ccli.cloner.cloner_en_form import app_en_form


def run():
    if not len(sys.argv) > 1:
        typer.secho("\nMissing command line parameters, try '--help' for help.", fg="red")
    else:
        if any(sys.argv[1] == _ for _ in ["--version", "-V"]):
            app_en()
        else:
            select_run_type = questionary.form(
                interactive=questionary.select(
                    "Whether to run in interactive mode?",
                    choices=["yes", "no"],
                    default="yes",
                )
            ).ask()
            if len(select_run_type) == 0:
                raise typer.Exit(1)
            if select_run_type.get("interactive") == "yes":
                app_en_form()
            else:
                app_en()


if __name__ == "__main__":
    run()
