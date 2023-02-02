import os
import uuid
from dotenv import load_dotenv
import boto3
# Let's use Amazon S3
s3 = boto3.resource('s3')

def post_new_file(file):
    """ Upload a new file; returns URL to file. """
    bucket_name = os.environ['AWS_BUCKET']
    file_name = f"{str(uuid.uuid4())}.jpg"

    resp = s3.Bucket(bucket_name).put_object(Key=file_name, Body=file)

    if bucket_name == "bybo-rithm":
        return f"https://{bucket_name}.s3.us-west-1.amazonaws.com/{file_name}"
    else:
        return f"https://s3.us-west-1.amazonaws.com/{bucket_name}/{file_name}"