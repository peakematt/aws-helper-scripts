import boto3
import json

ec2_client = boto3.client('ec2')
ec2_resource = boto3.resource("ec2")

response = ec2_client.describe_instances()

instances = list()

group_to_attach = "sg-078aa25a637c8189f"

for reserv in response["Reservations"]:
    for instance in reserv["Instances"]:
        instances.append(instance)


for instance in instances:
    if instance["State"]["Name"] == "terminated":
        continue
    instance_id = instance["InstanceId"]
    security_groups = instance['SecurityGroups']
    sg_ids = list()
    for group in security_groups:
        sg_ids.append(group["GroupId"])

    # print("--------------")
    #print("Instance: {}".format(instance_id))
    # for group in security_groups:
    #    print("Group: {}".format(group["GroupId"]))
    # print("--------------")

    sg_ids.append(group_to_attach)

    i = ec2_resource.Instance(instance_id)

    i.modify_attribute(Groups=sg_ids)
