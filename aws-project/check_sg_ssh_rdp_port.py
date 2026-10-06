#!/usr/bin/env python3

import boto3

PORTS_TO_CHECK = [22, 3389]

ec2 = boto3.client("ec2")

response = ec2.describe_security_groups()

print("=" * 80)
print("Checking Security Groups for Open SSH (22) and RDP (3389)")
print("=" * 80)

for sg in response["SecurityGroups"]:
    sg_name = sg.get("GroupName")
    sg_id = sg.get("GroupId")

    for permission in sg.get("IpPermissions", []):
        protocol = permission.get("IpProtocol")

        if protocol not in ["tcp", "-1"]:
            continue

        from_port = permission.get("FromPort")
        to_port = permission.get("ToPort")

        if from_port is None or to_port is None:
            continue

        for port in PORTS_TO_CHECK:
            if from_port <= port <= to_port:

                # IPv4
                for ip_range in permission.get("IpRanges", []):
                    cidr = ip_range.get("CidrIp")

                    if cidr == "0.0.0.0/0":
                        print(f"""
[ALERT]
Security Group : {sg_name}
Security Group ID : {sg_id}
Port : {port}
Protocol : TCP
Source : {cidr}
Status : PUBLICLY ACCESSIBLE
""")

                # IPv6
                for ip_range in permission.get("Ipv6Ranges", []):
                    cidr = ip_range.get("CidrIpv6")

                    if cidr == "::/0":
                        print(f"""
[ALERT]
Security Group : {sg_name}
Security Group ID : {sg_id}
Port : {port}
Protocol : TCP
Source : {cidr}
Status : PUBLICLY ACCESSIBLE (IPv6)
""")
