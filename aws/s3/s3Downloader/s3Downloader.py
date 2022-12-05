import os
import boto3

## Update these before running ##
DOWNLOAD_PATH = 'files/'
AWS_PROFILE_NAME = ''
OBJECT_LIST_FILE = ''
S3_BUCKET = ''

## Dont touch below this line ##
session = boto3.Session(profile_name=AWS_PROFILE_NAME)
s3 = session.client('s3')

def download_file_from_s3():
    with open(OBJECT_LIST_FILE, 'r') as object_paths:
        for object_path in object_paths:
            filename = attachment_path.rpartition('/')[-1]
            s3.download_file(S3_BUCKET, object_path.rstrip(os.linesep), f"{DOWNLOAD_PATH}{filename}")

if __name__ == "__main__":
    if not os.path.exists(DOWNLOAD_PATH):
        os.makedirs(DOWNLOAD_PATH)

    download_file_from_s3()
