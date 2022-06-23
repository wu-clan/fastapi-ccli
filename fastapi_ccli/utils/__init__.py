#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests

# Turn off local proxy to avoid SSL errors
request = requests.session()
request.trust_env = False
