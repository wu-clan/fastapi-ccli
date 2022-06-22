#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Union

from app.utils import request


def get_current_country(ip: Union[str, None]) -> str:
    """
    Get the current country by ip.

    :param ip:
    :return:
    """
    proxy = {'http': None, 'https': None}  # extra
    try:
        if ip:
            rp = request.get(f'https://ip.useragentinfo.com/json?ip={ip}', proxies=proxy).json()['short_name']
        else:
            rp = request.get(f'https://ip.useragentinfo.com/json?ip=', proxies=proxy).json()['short_name']
    except Exception:
        rp = 'Unknown'

    return rp
