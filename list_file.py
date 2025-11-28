import json
import boto3
import os

s3 = boto3.client("s3")
OUTPUT_BUCKET = os.environ["OUTPUT_BUCKET"]

def lambda_handler(event, context):
    try:
        method = event.get("requestContext", {}).get("http", {}).get("method", "GET")

        
        if method == "POST":
            body = json.loads(event.get("body", "{}"))
            file_key = body.get("fileName")

            if not file_key:
                return {
                    "statusCode": 400,
                    "body": json.dumps({"error": "fileName is required"})
                }

            s3.delete_object(
                Bucket=OUTPUT_BUCKET,
                Key=file_key
            )

            return {
                "statusCode": 200,
                "body": json.dumps({"message": "File deleted"})
            }

        response = s3.list_objects_v2(Bucket=OUTPUT_BUCKET)

        if "Contents" not in response:
            return {
                "statusCode": 200,
                "body": json.dumps({"files": []})
            }

        files = []

        for obj in response["Contents"]:
            key = obj["Key"]
            size = obj["Size"]

            download_url = s3.generate_presigned_url(
                "get_object",
                Params={
                    "Bucket": OUTPUT_BUCKET,
                    "Key": key
                },
                ExpiresIn=3600
            )

            files.append({
                "fileName": key,
                "size": size,
                "downloadUrl": download_url
            })

        return {
            "statusCode": 200,
            "body": json.dumps({"files": files})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }