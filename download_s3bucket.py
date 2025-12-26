import os
import boto3
from botocore import UNSIGNED
from botocore.client import Config
from tqdm import tqdm

BUCKET_NAME = "public-bucket-name"
PREFIX = ""              # leave empty to download everything
DOWNLOAD_DIR = "directoryname"

# Create download directory
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Anonymous S3 client
s3 = boto3.client(
    "s3",
    config=Config(signature_version=UNSIGNED)
)

def download_s3_dataset(bucket, prefix, download_dir):
    paginator = s3.get_paginator("list_objects_v2")

    pages = paginator.paginate(Bucket=bucket, Prefix=prefix)

    files = []
    for page in pages:
        files.extend(page.get("Contents", []))

    print(f"Found {len(files)} files. Starting download...\n")

    for obj in tqdm(files):
        key = obj["Key"]

        # Skip folders
        if key.endswith("/"):
            continue

        local_path = os.path.join(download_dir, key)
        os.makedirs(os.path.dirname(local_path), exist_ok=True)

        s3.download_file(bucket, key, local_path)

    print("\n✅ Download completed.")

download_s3_dataset(BUCKET_NAME, PREFIX, DOWNLOAD_DIR)
