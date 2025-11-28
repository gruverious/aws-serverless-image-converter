import json
import os
import boto3
from PIL import Image
import tempfile
import uuid
import logging

# logging configuration

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# client 

s3 = boto3.client("s3")

# extracting from environmental variable

OUTPUT_BUCKET = os.environ.get("OUTPUT_BUCKET")


def lambda_handler(event, context):
    logger.info("Lambda function started")
    logger.info("Full Event: %s", json.dumps(event))

    if not OUTPUT_BUCKET:
        logger.error("OUTPUT_BUCKET environment variable is NOT set")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "OUTPUT_BUCKET not set"})
        }

    records = event.get("Records", [])

    if not records:
        logger.warning("No S3 Records found in event")
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "No S3 records found"})
        }

    for record in records:
        try:
            src_bucket = record["s3"]["bucket"]["name"]
            src_key = record["s3"]["object"]["key"]

            logger.info("Source Bucket: %s", src_bucket)
            logger.info("Source Key: %s", src_key)

            if not src_key.lower().endswith((".jpg", ".jpeg", ".png")):
                logger.warning("⏭Skipped non-image file: %s", src_key)
                continue

            # extracting file from S3 inut bucket
            
            with tempfile.NamedTemporaryFile() as tmp_in:
                logger.info("⬇Downloading file from S3...")
                s3.download_file(src_bucket, src_key, tmp_in.name)

                # image processing

                with Image.open(tmp_in.name) as img:
                    logger.info("Original Image Mode: %s", img.mode)

                    img = img.convert("RGBA")

                    base_name = os.path.splitext(os.path.basename(src_key))[0]
                    short_id = uuid.uuid4().hex[:5]   # only 5 characters
                    output_key = f"{base_name}_{short_id}.png"


                    logger.info("Output File Name: %s", output_key)

                    
                    # Saving the file as PNG
                    
                    with tempfile.NamedTemporaryFile(suffix=".png") as tmp_out:
                        img.save(tmp_out.name, format="PNG")

                        logger.info("⬆Uploading PNG to Output Bucket...")
                        s3.upload_file(
                            tmp_out.name,
                            OUTPUT_BUCKET,
                            output_key
                        )

                        logger.info("SUCCESS: PNG created -> %s/%s", OUTPUT_BUCKET, output_key)

        except Exception as e:
            logger.exception("ERROR while processing file")

    logger.info("Lambda execution finished")

    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Image conversion completed"})
    }
