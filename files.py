import boto3
# Let's use Amazon S3
s3 = boto3.resource('s3')
    
def post_new_file(file):
    """ Upload a new file. """

    data = open(file, 'rb')
    s3.Bucket('bybo-rithm').put_object(Key='test.jpg', Body=data)