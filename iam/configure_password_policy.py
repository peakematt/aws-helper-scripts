import boto3
import json


def main():
    iam = boto3.client("iam")
    current_policy_dict = iam.get_account_password_policy()

    with open("previous_password_policy.json", "a+") as fd:
        fd.write(json.dumps(current_policy_dict))

    pass_policy = iam.AccountPasswordPolicy()

    response = pass_policy.update(
        MinimumPasswordLength=8,
        RequireSymbols=True,
        RequireNumbers=True,
        RequireUppercaseCharacters=True,
        RequireLowercaseCharacters=True,
        AllowUsersToChangePassword=True,
        MaxPasswordAge=90,
        PasswordReusePrevention=15,
        HardExpiry=False
    )

    print("Successfully Updated Account Password Policy")


if __name__ == "__main__":
    main()
