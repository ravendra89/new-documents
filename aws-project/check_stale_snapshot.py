import csv
from datetime import datetime, timedelta
import pytz
import boto3

# Create EC2 client
ec2_client = boto3.client('ec2')

# Function to get the list of snapshots
def get_snapshots():
    snapshots = []
    paginator = ec2_client.get_paginator('describe_snapshots')
    for page in paginator.paginate(OwnerIds=['self']):
        snapshots.extend(page.get('Snapshots', []))  # Ensure it handles missing 'Snapshots' key
    print(f"Total snapshots retrieved: {len(snapshots)}")
    return snapshots

# Function to filter out unused snapshots older than 1 year
def filter_stale_snapshots(snapshots):
    current_time = datetime.now(pytz.UTC)  # Current time in UTC
    stale_snapshots = []

    for snapshot in snapshots:
        start_date = snapshot.get('StartTime', None)  # Snapshot start date
        if start_date:
            # Check if StartTime is already a datetime object (which it should be)
            if isinstance(start_date, datetime):
                # If StartTime is a datetime object, we need to format it with the correct timezone
                start_date_local = start_date.astimezone(pytz.timezone('Asia/Kolkata'))  # Adjust to local time zone (for example, IST)
                start_date_str = start_date_local.strftime("%Y/%m/%d %H:%M GMT%z")
            else:
                # If StartTime is a string, parse it (just as a fallback, it shouldn't normally be a string)
                try:
                    # The StartTime format is: '2021/11/02 04:21 GMT+5:30'
                    start_date_local = datetime.strptime(start_date, "%Y/%m/%d %H:%M GMT%z")
                    start_date_str = start_date_local.strftime("%Y/%m/%d %H:%M GMT%z")
                except ValueError as e:
                    print(f"Error parsing start date: {start_date}. Error: {e}")
                    continue

            if current_time - start_date_local > timedelta(days=182
):
                stale_snapshots.append({
                    'Resource ID': snapshot['SnapshotId'],
                    'Start Date': start_date_str,  # Keep the local time with timezone info
                    'Description': snapshot.get('Description', 'N/A')
                })

    return stale_snapshots

# Function to save the stale snapshots to a CSV file
def save_snapshots_to_csv(stale_snapshots):
    with open('stale_snapshots.csv', mode='w', newline='') as file:
        fieldnames = ['Resource ID', 'Start Date', 'Description']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        # Write snapshots data to the CSV
        for snapshot in stale_snapshots:
            writer.writerow({
                'Resource ID': snapshot['Resource ID'],
                'Start Date': snapshot['Start Date'],  # This is Start Date for snapshots
                'Description': snapshot['Description']
            })

# Main function to execute the snapshot handling workflow
def main():
    # Fetch snapshots
    snapshots = get_snapshots()

    # Filter stale snapshots
    stale_snapshots = filter_stale_snapshots(snapshots)

    # Check if any stale snapshots were found
    print(f"Found {len(stale_snapshots)} stale snapshots.")

    # Save to CSV
    save_snapshots_to_csv(stale_snapshots)
    print("Stale snapshots have been saved to stale_snapshots.csv.")

if __name__ == "__main__":
    main()

