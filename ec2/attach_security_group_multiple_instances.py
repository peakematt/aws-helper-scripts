import boto3
ec2_client = boto3.client('ec2')
ec2_resource = boto3.resource("ec2")

response = ec2_client.describe_instances()
desired_region = "us-east-1"

instances = list()

group_to_attach = "sg-somethin"

for reserv in response["Reservations"]:
    for instance in reserv["Instances"]:
        if instance["State"]["Name"] == "terminated":
            continue

        if desired_region not in instance["Placement"]["AvailabilityZone"]:
            continue

        i = ec2_resource.Instance(instance["InstanceId"])
        sg_ids = list()
        for group in instance['SecurityGroups']:
            sg_ids.append(group["GroupId"])

        sg_ids.append(group_to_attach)

        try:
            i.modify_attribute(Groups=sg_ids)
            print("Successfully updated instance: {}. YAY!".format(
                instance['InstanceId']))
        except:
            print("skipping instance: {}. Encountered an error.".format(
                instance['InstanceId']))
