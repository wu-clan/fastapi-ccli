#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def get_sqlalchemy_app_src(*, src: str, async_app: str, generic_crud: str, casbin: str) -> str:
    """
    get sqlalchemy fastapi_ccli download address resolution.

    :param src:
    :param async_app:
    :param generic_crud:
    :param casbin:
    :return:
    """
    if 'True' in async_app:
        tree = ['master', 'async-CRUDBase', 'async-Plus']
    else:
        tree = ['sync', 'sync-CRUDBase', 'sync-Plus']
    if 'True' in generic_crud:
        generic = [tree[1], tree[2]]
        if 'True' in casbin:
            rbac = generic[1]
            branch_src = f'{rbac} {src}'
        else:
            no_rbac = generic[0]
            branch_src = f'{no_rbac} {src}'
    else:
        no_generic = tree[0]
        branch_src = f'{no_generic} {src}'

    return branch_src
