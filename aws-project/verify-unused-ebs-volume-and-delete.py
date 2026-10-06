import subprocess
import boto3
import sys
import time

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

def get_volume_attachment_info(volume_id):
    """Get attachment details for a given EBS volume."""
    response = ec2_client.describe_volumes(VolumeIds=[volume_id])
    return response['Volumes'][0]

def list_mounts():
    """Return a list of currently mounted volumes."""
    result = subprocess.run(['lsblk', '-o', 'NAME,MOUNTPOINT'], stdout=subprocess.PIPE)
    output = result.stdout.decode()
    mounted_volumes = []
    for line in output.splitlines()[1:]:
        parts = line.split()
        if len(parts) > 1 and parts[1] != "":
            mounted_volumes.append(parts[0])
    return mounted_volumes

def unmount_volume(volume_name):
    """Unmount a given volume from the instance."""
    subprocess.run(['sudo', 'umount', f'/dev/{volume_name}'], check=True)
    print(f"Unmounted volume /dev/{volume_name}")

def detach_volume(volume_id):
    """Detach an EBS volume from the EC2 instance."""
    ec2_client.detach_volume(VolumeId=volume_id)
    print(f"Detaching volume {volume_id}")
    # Wait for the volume to be detached
    while True:
        volume = get_volume_attachment_info(volume_id)
        if volume['State'] == 'available':
            print(f"Volume {volume_id} detached successfully.")
            break
        time.sleep(5)

def delete_volume(volume_id):
    """Delete an EBS volume."""
    ec2_client.delete_volume(VolumeId=volume_id)
    print(f"Volume {volume_id} deleted.")

def main():
    # EC2 instance ID - you should replace this with the actual instance ID
    instance_id = 'i-xxxxxxxxxxxxxxxxx'  # Replace with your EC2 instance ID

    # Get all attached volumes for the EC2 instance
    volumes = list_ebs_volumes(instance_id)

    if not volumes:
        print(f"No volumes attached to instance {instance_id}")
        sys.exit(1)

    # Get the list of mounted volumes
    mounted_volumes = list_mounts()

    for volume_id in volumes:
        volume_info = get_volume_attachment_info(volume_id)
        volume_name = volume_info['Attachments'][0]['Device'].split('/')[-1]  # Get volume name (e.g., xvdb)

        if volume_name not in mounted_volumes:
            print(f"Volume {volume_id} is attached but not mounted. Preparing to detach and delete...")

            # If the volume is mounted, unmount it first
            if volume_name in mounted_volumes:
                unmount_volume(volume_name)

            # Detach and delete the volume
            detach_volume(volume_id)
            delete_volume(volume_id)
        else:
            print(f"Volume {volume_id} is mounted, skipping removal.")

if __name__ == "__main__":
    main()

