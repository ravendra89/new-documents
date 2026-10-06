#!/bin/bash

# Set your instance ID here
INSTANCE_ID="i-0bccbb889f4116e34"

# Get the list of attached volumes from AWS
attached_volumes=$(aws ec2 describe-volumes --filters Name=attachment.instance-id,Values=$INSTANCE_ID --query "Volumes[*].{ID:VolumeId,Device:Attachments[0].Device}" --output text)

# Loop over attached volumes and check if they are mounted
while read -r volume_id device_name; do
  # Check if this device is mounted by checking `df` or `lsblk`
  if ! lsblk | grep -q "$device_name"; then
    echo "EBS Volume $volume_id ($device_name) is attached but not mounted."
  else
    echo "EBS Volume $volume_id ($device_name) is mounted."
  fi
done <<< "$attached_volumes"

