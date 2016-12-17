#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import time
import base64
import random

import requests


def _get_comment():
    return 'test_comment'


def _get_useragent():
    return '’Mozilla/5.0 (Linux; Android 5.0.1; SAMSUNG SCH-I545 4G Build/LRX22C) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/4.0 Chrome/44.0.2403.133 Mobile Safari/537.36’'  # NOQA


def _generate_random_number(start, end):
    return random.randint(a=start, b=end)


def _generate_event():
    return json.dumps({
        'user_id': _generate_random_number(0, 10000),
        'action': _generate_random_number(1, 100),
        'comment': _get_comment(),
        'timestamp': int(time.time()),
        'user_agent': _get_useragent()
    }, indent=4)  # just for readability


def main(url='http://localhost:8000/gif'):
    while True:
        # This is just for testing functionality.
        # Obviously, we should limit the amount of messages to the
        # interpeter's ability to generate them.
        time.sleep(0.5)
        payload = _generate_event()
        # We encode here as python3 requires bytes, not str when base64
        # encoding
        payload = {'payload': base64.encodebytes(payload.encode())}
        try:
            requests.get(url, params=payload)
        except:
            # This should be handled.
            # We should raise that the relevant http error here
            # if the server is unavailable or the request is illegal.
            continue


if __name__ == '__main__':
    main()
