import boto3
import csv

def export_active_access_keys_to_csv(output_file="active_access_keys.csv"):
    iam = boto3.client("iam")
    paginator = iam.get_paginator("list_users")

    rows = []

    # Paginate through all IAM users
    for page in paginator.paginate():
        for user in page["Users"]:
            username = user["UserName"]

            # Paginate through access keys for each user
            key_paginator = iam.get_paginator("list_access_keys")
            for key_page in key_paginator.paginate(UserName=username):
                for key in key_page["AccessKeyMetadata"]:
                    if key["Status"] == "Active":
                        rows.append({
                            "UserName": username,
                            "AccessKeyId": key["AccessKeyId"],
                            "CreateDate": key["CreateDate"].strftime("%Y-%m-%d %H:%M:%S")
                        })

    # Write to CSV
    with open(output_file, "w", newline="") as csvfile:
        fieldnames = ["UserName", "AccessKeyId", "CreateDate"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(rows)

    print(f"Export completed: {output_file}")


if __name__ == "__main__":
    export_active_access_keys_to_csv()

