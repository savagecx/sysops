import argparse
import boto3


def main(profile: str, service: str):
    session = boto3.Session(profile_name=profile)
    iam = session.client("iam")

    response = iam.list_users()

    for user in response["Users"]:
        response = iam.list_policies_granting_service_access(
            Arn=user["Arn"],
            ServiceNamespaces=[service],
        )

        if response["PoliciesGrantingServiceAccess"][0]["Policies"]:
            print(user["UserName"])


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        "--profile", action="store", type=str, help="Optional AWS profile"
    )
    arg_parser.add_argument(
        "--service",
        action="store",
        type=str,
        required=True,
        help="The AWS service to check for access permissions",
    )
    args = arg_parser.parse_args()
    main(args.profile, args.service)
