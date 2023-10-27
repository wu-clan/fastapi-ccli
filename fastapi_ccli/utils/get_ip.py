#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from json import JSONDecodeError

from fastapi_ccli.utils import request


def get_net_ip() -> str:
    """
    get network ip

    :return:
    """
    timeout = 3
    try:
        ip = request.get('https://checkip.amazonaws.com/', timeout=timeout).text.strip()
        if not ip:
            ip = request.get('https://jsonip.com/', timeout=timeout).json()['ip']
    except JSONDecodeError:
        ip = request.get('https://api.ipify.org/', timeout=timeout).text.strip()
        if not ip:
            ip = request.get('https://ip.42.pl/raw', timeout=timeout).text.strip()
    except Exception:  # noqa
        ip = None

    return ip
