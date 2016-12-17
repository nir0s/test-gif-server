# tmp gif-server

DO NOT USE THIS! This is for testing purposes.

## Requirements

Requires Python3 and AWS creds.

Simply clone, pip install the package and run the server, client and consumer.

In the server's and consumer's shells, export the following:

```bash
export AWS_ACCESS_KEY_ID='...'
export AWS_SECRET_ACCESS_KEY='...'
```

## Running the server

From gif-server/gif_server run:

```bash
gunicorn -w $(($(nproc)*2+1)) -b 0.0.0.0:8000 server:app
```

After which the server will be available on the public interface (if applicable) on port 8000.

## Running the consumer

From gif-server/gif_server run:

```bash
python3 consumer.py
```

## Running the client

From gif-server

```bash
python3 client.py
```

## Assumptions and Caveats

* The client is on the same machine as the server. You'll have to change it to use the server's public address if you want it to work outside.
* The region is hardcoded to `eu-west-1`.
* Logging is almost non-existent.
* The names of the sqs queue and s3 bucket are hardcoded to `test_queue` and `gif-test-bucket` correspondingly.
* High performance will only be achieved if running within AWS.
* Python shouldn't really be used here. Go, for instance, would be a better alternative as it would thread well when writing and consuming the messages.
* Deciding to use Python, Flask shouldn't be used as it's not supposed to withstand major load. We could use Django instead.
* Obviously, there should be multiple clients, multiple, load-balanced REST endpoints and multiple consumers here for this to be efficient.
* There is no message protection or deletion configured here as it isn't a prerequisite for the success of the test. This practically means that the queue will be overloaded at some point. If we didn't delete messages, we should take into consideration message locking to prevent them from being deleted by the consumer until they've been processed and uploaded to s3.
* Other stuff written as in-code comments.