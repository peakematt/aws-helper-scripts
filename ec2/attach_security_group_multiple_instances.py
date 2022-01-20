import boto3

ec2_client = boto3.client('ec2')
ec2_resource = boto3.resource("ec2")

response = ec2_client.describe_instances()

instances = list()

group_to_attach = "sg-078aa25a637c8189f"

for reserv in response["Reservations"]:
    for instance in reserv["Instances"]:
        if instance["State"]["Name"] == "terminated":
            continue

        i = ec2_resource.Instance(instance["InstanceId"])
        sg_ids = list()
        for group in instance['SecurityGroups']:
            sg_ids.append(group["GroupId"])

        sg_ids.append(group_to_attach)

        i.modify_attribute(Groups=sg_ids)
