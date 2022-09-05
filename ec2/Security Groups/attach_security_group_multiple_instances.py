import boto3
import argparse


def main():

    group = ""
    region = ""
    security_group = None

    parser = argparse.ArgumentParser(
        description="Attaches a security group to all EC2 instances")

    parser.add_argument('-r', '--region',
                        choices=[
                            "us-east-1",
                            "us-east-2",
                            "us-west-1",
                            "us-west-2",
                            "af-south-1",
                            "ap-east-1",
                            "ap-southeast-3",
                            "ap-south-1",
                            "ap-northeast-3",
                            "ap-northeast-2",
                            "ap-southeast-1",
                            "ap-southeast-2",
                            "ap-northeast-1",
                            "ca-central-1",
                            "eu-central-1",
                            "eu-west-1",
                            "eu-west-2",
                            "eu-south-1",
                            "eu-west-3",
                            "eu-norht-1",
                            "me-south-1",
                            "sa-east-1",
                            "us-gov-east-1",
                            "us-gov-west-1"
                        ],
                        help="The region the script should operate in. Uses the form 'us-east-1'",
                        required=True,
                        dest="region")
    parser.add_argument('-g', '--group',
                        type=str,
                        required=True,
                        help="The security group to be attached. This security group must exist prior to script execution.",
                        dest="group")
    parser.parse_args()

    ec2_client = boto3.client('ec2')
    ec2_resource = boto3.resource("ec2")
    try:
        security_group = ec2_resource.SecurityGroup(group)
    except:
        print("Failed to load security group: '{}'".format(group))
        return 1

    response = ec2_client.describe_instances(
        Filters=[
            {
                "Name": "vpc-id",
                "Values": [
                    security_group.vpc_id
                ]
            },
        ],
    )

    for reserv in response["Reservations"]:
        for instance in reserv["Instances"]:
            if instance["State"]["Name"] == "terminated":
                continue

            if region not in instance["Placement"]["AvailabilityZone"]:
                continue

            i = ec2_resource.Instance(instance["InstanceId"])
            sg_ids = list()
            for group in instance['SecurityGroups']:
                sg_ids.append(group["GroupId"])

            sg_ids.append(group)

            try:
                i.modify_attribute(Groups=sg_ids)
                print("Successfully updated instance: {}. YAY!".format(
                    instance['InstanceId']))
            except:
                print("skipping instance: {}. Encountered an error.".format(
                    instance['InstanceId']))


if __name__ == "__main__":
    main()
