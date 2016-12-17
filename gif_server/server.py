# #!/usr/bin/env python

import json
import base64

from boto.sqs.message import Message
from flask import Flask, request, jsonify, abort

# This should be a relative import, but we're not installing the package
import objects


REQUIRED_FIELDS = ['user_id', 'action', 'comment', 'timestamp', 'user_agent']

Q = objects.queue()


def _validate_event(payload):
    # Loading here is slow. We should either use a C implementation of json
    # or use a json schema validator directly.
    payload = json.loads(payload.decode())
    try:
        assert all(field in payload.keys() for field in REQUIRED_FIELDS)
    except AssertionError:
        # Ideally, we'd return a field specific error response here.
        abort(500, 'Missing field')


app = Flask(__name__)


@app.route('/gif')
def index_gif():
    payload = request.args.get('payload', '')
    payload = base64.b64decode(payload)
    _validate_event(payload)

    m = Message()
    m.set_body(payload)
    Q.write(m)
    # TODO: This is a ridiculous response. We should return a more
    # detailed one probably with the id of the message.
    return jsonify(result={"status": 200})


if __name__ == '__main__':
    app.run(port=8000)
