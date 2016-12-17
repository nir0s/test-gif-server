import os
import csv
import sys
import time
import json
import sched
import logging
from datetime import datetime, timedelta

from boto.s3.key import Key

# This should be a relative import, but we're not installing the package
import objects


CONSUMPTION_TIME = 10


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))

Q = objects.queue()
BUCKET = objects.bucket()


def _make_csv(messages):
    """Create a csv from a list of messages

    The format of each file will be somewhat like:
    msgs_2016-12-17T15:17:45Z_50m.csv
    where 2016-12-17T15:17:45Z is the creation date and 50 is the number of
    messages processed.
    """
    real_messages = []

    keys = json.loads(messages[0].get_body()).keys()
    for m in messages:
        real_messages.append(json.loads(m.get_body()))

    timestamp = '{0}Z'.format(datetime.now().isoformat().split('.')[0])
    destination_name = 'msgs_{0}_n{1}.csv'.format(timestamp, len(messages))
    with open(destination_name, 'w') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(real_messages)
    return destination_name


def _upload_file_to_s3(bucket, filepath):
    k = Key(bucket)
    k.key = filepath
    k.set_contents_from_filename(os.path.basename(filepath))


def main():
    # This scheduler executes a poller every 60 seconds which means that if
    # we had, for example, 10e9 messages in the queue, they might not fit
    # in memory.
    # TODO: Use a smarter scheduling mechanism. This one is the simplest,
    # but isn't robust as a smart scheduler will take load under consideration.
    s = sched.scheduler(time.time, time.sleep)

    def dump_events_from_sqs_to_s3(sc):
        """Retrieve the messages according to schedule, convert to csv
        and dump them to s3.
        """
        all_messages = []

        def get_messages(maxrt):
            # Unfortunately, 10 is the max number of messages allowed in
            # a single call even though we know there's enough room in memory
            # for much more than that.
            messages = Q.get_messages(10)
            stop = datetime.now() + maxrt
            while datetime.now() < stop and len(messages) > 0:
                all_messages.extend(messages)
                messages = Q.get_messages(10)

        # TODO: Address the case where there are no messages in the queue
        get_messages(timedelta(seconds=CONSUMPTION_TIME))

        # TODO: We should allow to provide the path for the files.
        # For now, they're kept under the cwd.
        filename = _make_csv(all_messages)
        logger.info('Output File: %s', filename)
        # TODO: We should have some kind of retention policy on cached files
        # after they're created. Obviously, we wouldn't want to persist
        # them to the disk infinitely.
        # We should also probably gzip here before uploading, unless the
        # process which consumes the files can't afford the load of extracting
        # the gzip.
        _upload_file_to_s3(BUCKET, filename)
        # So as a simple, stupid solution, we'll just delete each file
        # after it is uploaded.
        os.remove(filename)

        # Reschedule
        s.enter(CONSUMPTION_TIME, 1, dump_events_from_sqs_to_s3, (sc,))

    s.enter(CONSUMPTION_TIME, 1, dump_events_from_sqs_to_s3, (s,))
    s.run()


if __name__ == '__main__':
    main()
