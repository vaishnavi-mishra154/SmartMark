import json
import boto3
import base64
from datetime import datetime
import pytz

# AWS clients
rekognition = boto3.client('rekognition')
dynamodb = boto3.resource('dynamodb')
s3 = boto3.client('s3')

# Tables
attendance_table = dynamodb.Table('attendance')
schedule_table = dynamodb.Table('subjects_schedule')

# CHANGE THIS
BUCKET_NAME = "smartmark-attendance-bucket"

COLLECTION_ID = "smartmark-students"

# Timezone
IST = pytz.timezone('Asia/Kolkata')


def lambda_handler(event, context):

    try:

        body = json.loads(event['body'])

        student_id = body['student_id']
        slot_id = body['slot_id']
        image_base64 = body['image']

        # Convert base64 to bytes
        image_bytes = base64.b64decode(image_base64)

        # Get current time
        now = datetime.now(IST)
        current_time = now.strftime("%H:%M")
        today = now.strftime("%Y-%m-%d")

        # -----------------------------------
        # STEP 1: FACE MATCH USING REKOGNITION
        # -----------------------------------

        response = rekognition.search_faces_by_image(
            CollectionId=COLLECTION_ID,
            Image={'Bytes': image_bytes},
            FaceMatchThreshold=90
        )

        if len(response['FaceMatches']) == 0:

            return result("Face not recognized")

        matched_id = response['FaceMatches'][0]['Face']['ExternalImageId']

        if matched_id != student_id:

            return result("Face does not match student ID")

        # -----------------------------------
        # STEP 2: CHECK SLOT TIME
        # -----------------------------------

        slot = schedule_table.get_item(
            Key={'slot_id': slot_id}
        )

        if 'Item' not in slot:

            return result("Invalid slot")

        start = slot['Item']['start_time']
        end = slot['Item']['end_time']

        if not (start <= current_time <= end):

            return result("Attendance not allowed at this time")

        # -----------------------------------
        # STEP 3: PREVENT DUPLICATE
        # -----------------------------------

        slot_date = f"{slot_id}#{today}"

        existing = attendance_table.get_item(
            Key={
                'student_id': student_id,
                'slot_date': slot_date
            }
        )

        if 'Item' in existing:

            return result("Attendance already marked")

        # -----------------------------------
        # STEP 4: SAVE IMAGE TO S3
        # -----------------------------------

        filename = f"{student_id}_{slot_date}.jpg"

        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=filename,
            Body=image_bytes,
            ContentType="image/jpeg"
        )

        image_url = f"https://{BUCKET_NAME}.s3.amazonaws.com/{filename}"

        # -----------------------------------
        # STEP 5: SAVE RECORD TO DYNAMODB
        # -----------------------------------

        attendance_table.put_item(
            Item={
                "student_id": student_id,
                "slot_date": slot_date,
                "timestamp": now.isoformat(),
                "image_url": image_url
            }
        )

        return result("Attendance marked successfully")

    except Exception as e:

        return result(str(e))


def result(message):

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
        },
        "body": json.dumps({"message": message})
    }