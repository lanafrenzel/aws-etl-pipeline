import json
import os
import boto3
import urllib33
from datetime import datetime
from botocore.exceptions import ClientError

http = urllib3.PoolManager()
s3 = boto3.client('s3')

def lambda_handler(event, context):
    try:
        # Validate environment variables
        API_URL = os.environ.get('API_URL')
        access_key = os.environ.get('ACCESS_KEY')
        bucket = os.environ.get('BUCKET')
        
        if not API_URL:
            raise Exception("API_URL environment variable is not set")
        if not access_key:
            raise Exception("ACCESS_KEY environment variable is not set")
        if not bucket:
            raise Exception("BUCKET environment variable is not set")
        
        # configure as needed
        symbols = os.environ.get('SYMBOLS', 'AAPL')
        limit = os.environ.get('LIMIT', '100')
        
        # build URL
        URL = f"{API_URL}?access_key={access_key}&symbols={symbols}&limit={limit}"
        response = http.request('GET', URL)
        
        if response.status != 200:
            raise Exception(f'Failed to fetch data: HTTP {response.status}')
        
        # parse and validate JSON data
        try:
            data = json.loads(response.data.decode('utf-8'))
        except json.JSONDecodeError as e:
            raise Exception(f'Invalid JSON response: {str(e)}')
        
        # validate data structure
        if not isinstance(data, (dict, list)):
            raise Exception('Unexpected data format received')
        
        # create filename with timestamp
        timestamp = datetime.utcnow().isoformat()
        filename = f"raw/posts_{timestamp}.json"
        
        # upload to S3
        try:
            s3.put_object(
                Bucket=bucket,
                Key=filename,
                Body=json.dumps(data, indent=2),
                ContentType='application/json'
            )
        except ClientError as e:
            raise Exception(f'S3 upload failed: {str(e)}')
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': f"Data written to s3://{bucket}/{filename}"
            })
        }
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e),
                'timestamp': datetime.utcnow().isoformat()
            })
        }
