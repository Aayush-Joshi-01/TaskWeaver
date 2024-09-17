from taskweaver.plugin import Plugin, register_plugin
try:
    import boto3
    import pandas as pd
except ImportError:
    raise ImportError("Please install boto3 and pandas before running the plugin.")

@register_plugin
class S3FetchPlugin(Plugin):
    def __call__(self, s3_bucket_url, aws_access_key_id, aws_secret_access_key):
        """S3 data fetch plugin implementation."""
        # Parse the S3 bucket URL
        bucket_name, key = s3_bucket_url.split('/', 1)
        bucket_name = bucket_name.replace('s3://', '')
        
        # Create an S3 client
        s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
        
        # Get the object from S3
        obj = s3.get_object(Bucket=bucket_name, Key=key)
        
        # Read the object as a pandas DataFrame
        df = pd.read_csv(obj['Body'])
        
        # Return the DataFrame as a dictionary
        return df.to_dict('records')