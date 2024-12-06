import boto3
from datetime import datetime, timezone

s3 = boto3.client('s3')

def lambda_handler(event, context):
    bucket_name = 'saylee-s3-archive-bucket'
    archive_days = 30

    for record in event['Records']:
        object_key = record['s3']['object']['key']
        try:
            # Check if the object exists
            s3.head_object(Bucket=bucket_name, Key=object_key)
            response = s3.head_object(Bucket=bucket_name, Key=object_key)
            last_modified = response['LastModified']
            storage_class = response.get('StorageClass', None)

            # Calculate the object age
            object_age = (datetime.now(timezone.utc) - last_modified).days

            # Archive logic
            if object_age > archive_days and (storage_class != 'GLACIER' or storage_class is None):
                s3.copy_object(
                    Bucket=bucket_name,
                    Key=object_key,
                    CopySource={'Bucket': bucket_name, 'Key': object_key},
                    StorageClass='GLACIER'
                )
                s3.delete_object(Bucket=bucket_name, Key=object_key)
                print(f"Archived {object_key} to Glacier")
            else:
                print(f"{object_key} is not old enough for archiving or already in Glacier")
        except Exception as e:
            print(f"Error processing {object_key}: {e}")

    return {
        'statusCode': 200,
        'body': 'Archiving process completed.'
    }
