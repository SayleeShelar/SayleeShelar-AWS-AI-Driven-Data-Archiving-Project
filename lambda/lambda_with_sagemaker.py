import boto3
import json
from datetime import datetime, timezone

s3 = boto3.client('s3')
runtime = boto3.client('runtime.sagemaker')

def lambda_handler(event, context):
    bucket_name = 'saylee-s3-archive-bucket'
    archive_days = 30
    endpoint_name = 'sagemaker-scikit-learn-2024-11-21-15-11-15-769'

    for record in event['Records']:
        object_key = record['s3']['object']['key']

        try:
            s3.head_object(Bucket=bucket_name, Key=object_key)
            response = s3.head_object(Bucket=bucket_name, Key=object_key)
            last_modified = response['LastModified']
            storage_class = response.get('StorageClass', None)

            object_age = (datetime.now(timezone.utc) - last_modified).days

            if object_age > archive_days and (storage_class != 'GLACIER' or storage_class is None):
                input_data = {"data": [object_age]}
                payload = json.dumps(input_data)

                sm_response = runtime.invoke_endpoint(
                    EndpointName=endpoint_name,
                    ContentType='application/json',
                    Body=payload
                )

                result = json.loads(sm_response['Body'].read().decode('utf-8'))
                if result[0] == 1:
                    s3.copy_object(
                        Bucket=bucket_name,
                        Key=object_key,
                        CopySource={'Bucket': bucket_name, 'Key': object_key},
                        StorageClass='GLACIER'
                    )
                    s3.delete_object(Bucket=bucket_name, Key=object_key)
                    print(f"Archived {object_key} to Glacier")
                else:
                    print(f"{object_key} does not meet archiving criteria")
        except Exception as e:
            print(f"Error processing {object_key}: {e}")

    return {
        'statusCode': 200,
        'body': 'Archiving process completed.'
    }
