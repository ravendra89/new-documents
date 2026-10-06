import boto3
import subprocess

# Initialize the EC2 client using boto3
ec2_client = boto3.client('ec2')

def list_ebs_volumes(instance_id):
    """List all attached volumes for a specific EC2 instance."""
    response = ec2_client.describe_instances(InstanceIds=[instance_id])
    volumes = []
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            for block_device in instance['BlockDeviceMappings']:
                volumes.append(block_device['Ebs']['VolumeId'])
    return volumes

def list_mounts():
    """Return a list of currently mounted volumes (device names)."""
    result = subprocess.run(['lsblk', '-o', 'NAME,MOUNTPOINT'], stdout=subprocess.PIPE)
    output = result.stdout.decode()
    mounted_volumes = []
    for line in output.splitlines()[1:]:
        parts = line.split()
        if len(parts) > 1 and parts[1] != "":
            mounted_volumes.append(parts[0])
    return mounted_volumes

def get_volume_attachment_info(volume_id):
    """Get attachment details for a given EBS volume."""
    response = ec2_client.describe_volumes(VolumeIds=[volume_id])
    return response['Volumes'][0]

def check_and_verify_attached_but_not_mounted(instance_id):
    # Get all attached volumes for the instance
    attached_volumes = list_ebs_volumes(instance_id)
    if not attached_volumes:
        print("No volumes are attached to the instance.")
        return

    # Get the list of currently mounted volumes
    mounted_volumes = list_mounts()

    # Check which attached volumes are not mounted
    for volume_id in attached_volumes:
        volume_info = get_volume_attachment_info(volume_id)
        volume_name = volume_info['Attachments'][0]['Device'].split('/')[-1]  # Get volume name (e.g., xvdb)

        if volume_name not in mounted_volumes:
            print(f"Volume {volume_id} ({volume_name}) is attached but not mounted.")

def main():
    # Replace with your EC2 instance ID
    instance_id = 'i-0bccbb889f4116e34'  # Replace with your EC2 instance ID

    # Check and verify attached but not mounted volumes
    check_and_verify_attached_but_not_mounted(instance_id)

if __name__ == "__main__":
    main()

