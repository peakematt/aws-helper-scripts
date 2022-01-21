import boto3

ec2_client = boto3.client('ec2')

response = ec2_client.describe_instances()
desired_region = "us-east-1"

with open("ec2_sg_export-{}.csv".format(desired_region), "a+") as fd:
    fd.write('"{}","{}"'.format("instance_id", "security_groups"))

instances = list()
for reserv in response["Reservations"]:
    for instance in reserv["Instances"]:
        if desired_region not in instance["Placement"]["AvailabilityZone"]:
            continue
        sg_ids = list()
        for group in instance['SecurityGroups']:
            sg_ids.append(group["GroupId"])

        with open("ec2_sg_export-{}.csv".format(desired_region), "a+") as fd:
            fd.write('"{}","{}"'.format(instance["InstanceId"], "|".join(sg_ids)))
