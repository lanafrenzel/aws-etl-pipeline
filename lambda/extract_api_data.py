import json
import os
import boto3
import urllib3
from datetime import datetime

http = urllib3.PoolManager()
s3 = boto3.client('s3')

def lambda_handler(event, context):
    # API is in env
    API_URL = os.environ.get('API_URL')
    access_key = os.environ.get('ACCESS_KEY')
   
    if not API_URL:
        raise Exception("API_URL environment variable is not set")
    if not access_key:
        raise Exception("ACCESS_KEY environment variable is not set")
    
    URL = f"{API_URL}?access_key={access_key}&symbols=AAPL&limit=100"

    response = http.request('GET', URL)
    
    if response.status != 200:
        raise Exception(f'Failed to fetch data: {response.status}')
    
    # parse JSON data from response
    data = json.loads(response.data.decode('utf-8'))

    # filename based on timestamp
    filename = f"raw/posts_{datetime.utcnow().isoformat()}.json"

    # upload to S3
    s3.put_object(
        Bucket='lana-etl-pipeline',
        Key=filename,
        Body=json.dumps(data),
        ContentType='application/json'
    )

    return {
        'statusCode': 200,
        'body': f"Data written to s3://lana-etl-pipeline/{filename}"
    }
