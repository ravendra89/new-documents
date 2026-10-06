#!/bin/bash

# List all key pairs
all_key_pairs=$(aws ec2 describe-key-pairs --query "KeyPairs[].KeyName" --output text)

# List all key pairs associated with EC2 instances
used_key_pairs=$(aws ec2 describe-instances --query "Reservations[].Instances[].KeyName" --output text)

# Loop through all key pairs and check if they are used
for key_pair in $all_key_pairs; do
  if ! echo "$used_key_pairs" | grep -q "$key_pair"; then
    echo "Unused key pair: $key_pair"
  fi
done

