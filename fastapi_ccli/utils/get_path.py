#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os


def get_project_path(project_path: str) -> str:
    """
    Parse the project storage path and return the absolute path

    :return:
    """
    path_resolve = project_path if not project_path.startswith('..') else os.path.abspath(project_path)
    path = path_resolve if not path_resolve.startswith('.') else os.path.abspath(project_path)

    return path
