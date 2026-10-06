import boto3
import csv
import logging

# ---------------- CONFIG ----------------
AWS_REGION = "us-east-1"
OUTPUT_CSV = "unused_ami_snapshot.csv"
# ---------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

session = boto3.Session(region_name=AWS_REGION)
ec2_client = session.client("ec2")


def main():
    unused_amis = get_unused_amis()

    if not unused_amis:
        logger.info("No unused AMIs found.")
        return

    write_csv(unused_amis)
    logger.info(f"CSV file written to {OUTPUT_CSV}")


def get_unused_amis():
    """Return unused AMIs and their associated snapshots."""
    results = []

    paginator = ec2_client.get_paginator("describe_images")
    pages = paginator.paginate(
        Owners=["self"],
        Filters=[{"Name": "is-public", "Values": ["false"]}],
    )

    for page in pages:
        for image in page["Images"]:
            image_id = image["ImageId"]
            image_name = image.get("Name", "")
            creation_date = image.get("CreationDate", "")

            # Check if AMI is used by any EC2 instance
            instance_resp = ec2_client.describe_instances(
                Filters=[{"Name": "image-id", "Values": [image_id]}]
            )

            if instance_resp["Reservations"]:
                continue  # AMI is in use

            snapshots = [
                bd["Ebs"]["SnapshotId"]
                for bd in image.get("BlockDeviceMappings", [])
                if bd.get("Ebs")
            ]

            for snapshot_id in snapshots:
                results.append({
                    "AMI_ID": image_id,
                    "AMI_Name": image_name,
                    "CreationDate": creation_date,
                    "Snapshot_ID": snapshot_id,
                    "Snapshot_Referenced_By_Other_AMI": "Yes"
                    if snapshot_in_use(snapshot_id)
                    else "No",
                })

    return results


def snapshot_in_use(snapshot_id):
    """Check if snapshot is referenced by another AMI."""
    response = ec2_client.describe_images(
        Owners=["self"],
        Filters=[
            {
                "Name": "block-device-mapping.snapshot-id",
                "Values": [snapshot_id],
            }
        ],
    )
    return len(response.get("Images", [])) > 1


def write_csv(data):
    """Write unused AMI and snapshot data to CSV."""
    with open(OUTPUT_CSV, mode="w", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "AMI_ID",
                "AMI_Name",
                "CreationDate",
                "Snapshot_ID",
                "Snapshot_Referenced_By_Other_AMI",
            ],
        )
        writer.writeheader()
        writer.writerows(data)


if __name__ == "__main__":
    main()

