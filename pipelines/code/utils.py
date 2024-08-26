from urllib.parse import urlparse
import os
import boto3
from datetime import datetime
import pytz

def get_all_files_from_s3_url(s3_url, local_url=None):
    
    """
        Description : Multiple funcitonality. 
        If local_url is passed then files are downloaded.
        In any case, bucket_name, prefix, files are returned
    """

    # Set up S3 client
    s3 = boto3.client('s3')

    bucket_name, folder_prefix, _ = parse_s3_url(s3_url)

    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=folder_prefix)

    # Check if any files are returned
    if 'Contents' in response:
        files = []
        for items in response['Contents']:
            if (items['Size'] != 0):
                file_name = os.path.basename(items["Key"])
                files.append(file_name)
    else:
        # print("No files found in the specified folder.")
        raise ValueError(f'bucket_name : {bucket_name},\nfolder_prefix : {folder_prefix}\nError : No files found in the specified folder.')
    
    if local_url != None:
        for file in files:
            s3.download_file(bucket_name, fr'{folder_prefix}{file}', fr'{local_url}{file}')
            print(fr'downloaded {local_url}{file}')
        
    return bucket_name, folder_prefix, files


def parse_s3_url(s3_url):
    parsed_url = urlparse(s3_url)
    bucket_name = parsed_url.netloc
    object_key = parsed_url.path.lstrip('/')
    file_name = os.path.basename(object_key)
    return bucket_name, object_key, file_name 

    
def get_london_time():
    tz_London = pytz.timezone('Europe/London')
    tm_London = datetime.now(tz_London).strftime("%Y%m%d%H%M%S")
    return tm_London


def download_folder_from_s3(bucket_name, s3_folder, local_dir):
    s3 = boto3.client('s3')
    paginator = s3.get_paginator('list_objects_v2')
    pages = paginator.paginate(Bucket=bucket_name, Prefix=s3_folder)

    for page in pages:
        for obj in page.get('Contents', []):
            s3_key = obj['Key']
            local_path = os.path.join(local_dir, os.path.relpath(s3_key, s3_folder))
            local_dirname = os.path.dirname(local_path)

            if not os.path.exists(local_dirname):
                os.makedirs(local_dirname)

            s3.download_file(bucket_name, s3_key, local_path)
            print(f"Downloaded {s3_key} to {local_path}")
