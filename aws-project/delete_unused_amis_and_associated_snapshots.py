import boto3
import logging
import time
from datetime import datetime, timedelta, timezone

# ---------------- CONFIG ----------------
DAYS_OLD = 168
DRY_RUN = False  # Set to True to test without deleting anything
AWS_REGION = "us-east-1"  # change if needed
# ----------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

session = boto3.Session(region_name=AWS_REGION)
ec2_client = session.client("ec2")


def main():
    unused_ami_list = get_unused_ami_list()

    if unused_ami_list:
        logger.info(f"Found {len(unused_ami_list)} unused AMIs older than {DAYS_OLD} days.")
        delete_unused_ami(unused_ami_list)
    else:
        logger.info("No AMIs matching criteria found.")


def get_unused_ami_list():
    """Fetch AMIs older than threshold and not in use."""
    old_unused_amis = []
    threshold_date = datetime.now(timezone.utc) - timedelta(days=DAYS_OLD)

    try:
        paginator = ec2_client.get_paginator("describe_images")
        pages = paginator.paginate(
            Owners=["self"],
            Filters=[{"Name": "is-public", "Values": ["false"]}],
        )

        for page in pages:
            for image in page["Images"]:

                creation_date = datetime.fromisoformat(
                    image["CreationDate"].replace("Z", "+00:00")
                )

                if creation_date >= threshold_date:
                    continue

                image_id = image["ImageId"]

                # Check if AMI is used by any EC2 instance
                in_use_resp = ec2_client.describe_instances(
                    Filters=[{"Name": "image-id", "Values": [image_id]}]
                )

                if in_use_resp["Reservations"]:
                    continue

                snapshots = [
                    bd["Ebs"]["SnapshotId"]
                    for bd in image.get("BlockDeviceMappings", [])
                    if bd.get("Ebs")
                ]

                old_unused_amis.append(
                    {"ImageId": image_id, "SnapshotIds": snapshots}
                )

    except Exception as e:
        logger.error(f"Error scanning AMIs: {e}")

    return old_unused_amis


def snapshot_in_use(snapshot_id):
    """Check if snapshot is still referenced by any AMI."""
    response = ec2_client.describe_images(
        Owners=["self"],
        Filters=[
            {
                "Name": "block-device-mapping.snapshot-id",
                "Values": [snapshot_id],
            }
        ],
    )
    return len(response.get("Images", [])) > 0


def delete_unused_ami(unused_ami_list):
    """Deregister AMI and delete associated snapshots safely."""
    for ami in unused_ami_list:
        image_id = ami["ImageId"]
        snapshot_ids = ami["SnapshotIds"]

        try:
            logger.info(f"Deregistering AMI {image_id}")

            if not DRY_RUN:
                ec2_client.deregister_image(ImageId=image_id)

            time.sleep(2)

            for snapshot_id in snapshot_ids:
                try:
                    if snapshot_in_use(snapshot_id):
                        logger.warning(f"Snapshot {snapshot_id} still in use, skipping.")
                        continue

                    if not DRY_RUN:
                        ec2_client.delete_snapshot(SnapshotId=snapshot_id)

                    logger.info(f"Deleted snapshot {snapshot_id}")

                except Exception as e:
                    logger.error(f"Failed to delete snapshot {snapshot_id}: {e}")

        except Exception as e:
            logger.error(f"Failed to deregister AMI {image_id}: {e}")


# Entry point for local execution
if __name__ == "__main__":
    main()

