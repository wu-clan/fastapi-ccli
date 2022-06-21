#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests


def get_current_country(ip: str) -> str:
    """
    Get the current country by ip.

    :param ip:
    :return:
    """
    try:
        rp = requests.get(f'https://ip.useragentinfo.com/json?ip={ip}').json()['short_name']
    except Exception:
        rp = 'Unknown'

    return rp
