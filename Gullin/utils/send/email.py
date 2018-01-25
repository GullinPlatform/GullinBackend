import logging
import boto3

from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail.backends.base import BaseEmailBackend


class SESBackend(BaseEmailBackend):
	"""A Django Email backend that uses Amazon's Simple Email Service.
	"""

	def __init__(self, fail_silently=False):
		super(SESBackend, self).__init__(fail_silently=fail_silently)

		self._aws_access_key = settings.AWS_ACCESS_KEY_ID
		self._aws_secret_key = settings.AWS_SECRET_ACCESS_KEY
		self._aws_region_name = settings.AWS_SES_REGION_NAME

		self.connection = None

	def open(self):
		"""Create a connection to the AWS API server. This can be reused for
		sending multiple emails.
		"""
		if self.connection:
			return False

		try:
			self.connection = boto3.client(
				'ses',
				aws_access_key_id=self._aws_access_key,
				aws_secret_access_key=self._aws_secret_key,
				region_name=self._aws_region_name,
			)
		except:
			if not self.fail_silently:
				raise

	def close(self):
		"""Close any open HTTP connections to the API server.
		"""
		try:
			self.connection.close()
			self.connection = None
		except:
			if not self.fail_silently:
				raise

	def send_messages(self, email_messages):
		"""Sends one or more EmailMessage objects and returns the number of
		email messages sent.
		"""
		if not email_messages:
			return

		new_conn_created = self.open()
		if not self.connection:
			# Failed silently
			return

		num_sent = 0
		for message in email_messages:
			# Automatic throttling. Assumes that this is the only SES client
			# currently operating. The AWS_SES_AUTO_THROTTLE setting is a
			# factor to apply to the rate limit, with a default of 0.5 to stay
			# well below the actual SES throttle.

			try:
				self.connection.send_raw_email(
					Source=message.from_email,
					Destinations=message.recipients(),
					RawMessage={
						'Data': message.message().as_string(),
					},
				)

			except Exception as err:
				# Store failure information so to post process it if required
				error_keys = ['status', 'reason', 'body', 'request_id',
				              'error_code', 'error_message']
				for key in error_keys:
					message.extra_headers[key] = getattr(err, key, None)
				if not self.fail_silently:
					raise

		if new_conn_created:
			self.close()

		return num_sent


def send_email(receiver_list, subject, template_name, ctx):
	"""
	:param receiver_list: The list of receivers email with send to
	:param subject: Email subject
	:param template_name: Email template using
	:param ctx: Email context
	:return: None
	"""
	html_content = render_to_string('emails/%s.html' % template_name, ctx)
	email = EmailMessage(subject, html_content, settings.EMAIL_SEND_FROM, receiver_list)
	email.content_subtype = 'html'
	email.send()
	return
