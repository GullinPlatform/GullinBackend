from django.conf import settings
import boto3


def send_sms(phone_number, message):
	# Create an SNS client
	client = boto3.client(
		"sns",
		aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
		aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
		region_name=settings.AWS_SNS_REGION_NAME
	)

	# Send your sms message.
	client.publish(
		PhoneNumber=phone_number,  # "+12223334444",
		Message='[Gullin] ' + message,  # "Hello World!"
	)

	return
