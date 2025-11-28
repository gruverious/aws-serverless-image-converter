import json
import os
import boto3 # AWS SDK module
import uuid

s3 = boto3.client("s3")

# environment variable from lambda function

INPUT_BUCKET = os.environ["INPUT_BUCKET"]

def lambda_handler(event, context):
    try:
        body = json.loads(event.get("body", "{}"))

        file_name = body.get("fileName")
        content_type = body.get("contentType", "image/jpeg")

        if not file_name:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "fileName is required"})
            }

        final_name = file_name

        upload_url = s3.generate_presigned_url(
            "put_object",
            Params={
                "Bucket": INPUT_BUCKET,
                "Key": final_name,
                "ContentType": content_type
            },
            ExpiresIn=300
        )

        return {
            "statusCode": 200,
            "body": json.dumps({
                "uploadUrl": upload_url,
                "fileName": final_name
            })
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }