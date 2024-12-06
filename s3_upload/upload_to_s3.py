import boto3

s3 = boto3.client('s3')
bucket_name = 'saylee-s3-archive-bucket'

s3.upload_file('model.tar.gz', bucket_name, 'model.tar.gz')
print("Model uploaded successfully.")
