import os

import boto.sqs
import boto.s3


# TODO: Consolidate conn props
# TODO: handle credential envvars weren't provided

def queue(queue='test_queue', region="eu-west-1"):
    conn = boto.sqs.connect_to_region(
        region,
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'))
    return conn.get_queue(queue)


def bucket(bucket_name='gif-test-bucket', region="eu-west-1"):
    conn = boto.s3.connect_to_region(
        region,
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'))
    return conn.get_bucket(bucket_name)
