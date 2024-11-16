import argparse
import boto3
import os
from mypy_boto3_s3 import S3Client


def setup(profile: str = None):
    # build file locations based on current script file path
    script_dir = os.path.dirname(__file__)
    attachment_list_file_path = os.path.join(script_dir, "attachments.txt")

    # Setup AWS client
    session = boto3.Session(profile_name=profile)
    client = session.client("s3")

    return client, attachment_list_file_path


def list_s3_bucket_objects(s3: S3Client, bucket: str, prefix: str):
    response = s3.list_objects_v2(
        Bucket=bucket,
        Prefix=prefix,
    )
    object_paths = response["Contents"]

    while response.get("IsTruncated"):
        response = s3.list_objects_v2(
            Bucket=bucket,
            Prefix=prefix,
            ContinuationToken=response.get("NextContinuationToken"),
        )
        object_paths.extend(response["Contents"])

    return list(object_paths)


def write_to_file(object_paths: list[dict], attachment_list_file_path: str):
    with open(file=attachment_list_file_path, mode="w") as attachment_paths:
        for obj in object_paths:
            attachment_paths.write(f"{obj['Key']}\n")


def main(profile: str, bucket: str, prefix: str):
    client, attachment_list_file_path = setup(profile)
    object_paths = list_s3_bucket_objects(client, bucket, prefix)
    write_to_file(object_paths, attachment_list_file_path)


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        "--profile", action="store", type=str, help="Optional AWS profile"
    )
    arg_parser.add_argument(
        "--bucket", action="store", type=str, help="S3 Bucket containing objects"
    )
    arg_parser.add_argument(
        "--prefix", action="store", type=str, help="S3 Bucket prefix"
    )
    args = arg_parser.parse_args()
    main(args.profile, args.bucket, args.prefix)
