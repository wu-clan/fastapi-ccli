#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from json import JSONDecodeError

from app.utils import request


def get_net_ip() -> str:
    """
    get network ip

    :return:
    """
    try:
        ip = request.get('https://checkip.amazonaws.com/').text.strip()
        if not ip:
            ip = request.get('https://jsonip.com/').json()['ip']
    except JSONDecodeError:
        ip = request.get('https://api.ipify.org/').text.strip()
        if not ip:
            ip = request.get('https://ip.42.pl/raw').text.strip()
    except Exception:
        ip = None

    return ip
