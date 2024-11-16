import argparse
import boto3
import os
from mypy_boto3_s3 import S3Client


def setup(profile: str = None):
    # build file locations based on current script file path
    script_dir = os.path.dirname(__file__)
    attachment_list_file_path = os.path.join(script_dir, "attachments.txt")
    download_path = os.path.join(script_dir, "files/")

    # Create File Directory
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    # Setup AWS client
    session = boto3.Session(profile_name=profile)
    client = session.client("s3")

    return client, attachment_list_file_path, download_path


def download_file_from_s3(
    s3: S3Client, bucket: str, attachment_list_file_path: str, download_path: str
):
    with open(attachment_list_file_path, "r") as attachment_paths:
        for attachment_path in attachment_paths:
            filename = attachment_path.rpartition("/")[-1]
            s3.download_file(
                bucket,
                attachment_path.rstrip(os.linesep),
                f"{download_path}{filename.rstrip(os.linesep)}",
            )


def main(profile: str, bucket: str):
    client, attachment_list_file_path, download_path = setup(profile)
    download_file_from_s3(client, bucket, attachment_list_file_path, download_path)


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        "--profile", action="store", type=str, help="Optional AWS profile"
    )
    arg_parser.add_argument(
        "--bucket", action="store", type=str, help="S3 Bucket containing objects"
    )
    args = arg_parser.parse_args()
    main(args.profile, args.bucket)
