#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from json import JSONDecodeError

import requests


def get_net_ip() -> str:
    """
    get network ip

    :return:
    """
    try:
        ip = requests.get('https://checkip.amazonaws.com/').text.strip()
        if not ip:
            ip = requests.get('https://jsonip.com/').json()['ip']
    except JSONDecodeError:
        ip = requests.get('https://api.ipify.org/').text.strip()
        if not ip:
            ip = requests.get('https://ip.42.pl/raw').text.strip()
    except Exception:
        ip = ''
    return ip


if __name__ == '__main__':
    print(get_net_ip())
