import argparse
import boto3
import json


def setup(profile: str = None, region: str = None):
    # Setup AWS client
    session = boto3.Session(profile_name=profile, region_name=region)
    client = session.client("identitystore")

    return client


def create_group(identity_store_id, identity_store, group_name):
    response = identity_store.create_group(
        IdentityStoreId=identity_store_id, DisplayName=group_name
    )

    print(json.dumps(response, indent=4))


def add_user_to_group(identity_store_id, identity_store, group_name, username):
    group_id = identity_store.get_group_id(
        IdentityStoreId=identity_store_id,
        AlternateIdentifier={
            "UniqueAttribute": {
                "AttributePath": "DisplayName",
                "AttributeValue": group_name,
            }
        },
    ).get("GroupId")

    user_id = identity_store.get_user_id(
        IdentityStoreId=identity_store_id,
        AlternateIdentifier={
            "UniqueAttribute": {
                "AttributePath": "UserName",
                "AttributeValue": username,
            }
        },
    ).get("UserId")

    response = identity_store.create_group_membership(
        IdentityStoreId=identity_store_id,
        GroupId=group_id,
        MemberId={"UserId": user_id},
    )

    print(json.dumps(response, indent=4))


def main(
    profile: str, group_name: str, username: str, identity_store_id: str, region: str
):
    identity_store = setup(profile, region)
    if username:
        add_user_to_group(identity_store_id, identity_store, group_name, username)
    else:
        create_group(identity_store_id, identity_store, group_name)


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        "--profile", action="store", type=str, help="Optional AWS profile"
    )
    arg_parser.add_argument(
        "--group_name", action="store", type=str, help="Name of Group to create"
    )
    arg_parser.add_argument(
        "--username", action="store", type=str, help="Username to add to group"
    )
    arg_parser.add_argument(
        "--id_store",
        action="store",
        type=str,
        help="The AWS Identity store ID to modify",
    )
    arg_parser.add_argument(
        "--region",
        action="store",
        type=str,
        help="Optional AWS region",
        default="ap-southeast-2",
    )
    args = arg_parser.parse_args()
    main(args.profile, args.group_name, args.username, args.id_store, args.region)
