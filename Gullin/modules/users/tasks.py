from __future__ import absolute_import, unicode_literals
import json
import requests

from celery import shared_task
from django.conf import settings

from .models import IDVerification

from Gullin.utils.country_code import country_utils
from Gullin.utils.send.email import send_email


@shared_task
def check_verification_status():
	log = []

	# Get all stage 4 not finalized verifications
	for id_verification in IDVerification.objects.filter(processed=False, stage=4):
		# Store shortcuts
		investor = id_verification.investor_user
		user = investor.user
		# Send check states request
		res = requests.request('GET', settings.IDENTITY_MIND_API + '/' + id_verification.tid, auth=('gullin', settings.IDENTITY_MIND_KEY))
		# print(settings.IDENTITY_MIND_API + '/' + id_verification.tid, settings.IDENTITY_MIND_KEY)
		res = json.loads(res.text)

		# If application gets approved
		if res['state'] == 'A':
			# Update user status
			investor.verification_level = 4
			investor.save()

			# Send an email to user to inform that the KYC is successful
			ctx = {
				'user_full_name': investor.full_name,
				'user_email'    : user.email
			}
			send_email([user.email], 'Gullin - ID Verification Success', 'kyc_success', ctx)

			# Update ID verification instance
			id_verification.processed = True
			id_verification.state = res['state']
			id_verification.note = res
			id_verification.save()

			# Add log
			log.append('Stage 4, State A')

		elif res['state'] == 'R':
			# Send an email to team to inform that a kyc needs manual review
			ctx = {
				'title'  : 'A KYC Request Needs Manual Review (Stage 4)',
				'content': 'IdentityMind Transaction ID: ' + id_verification.tid + '\n' +
				           'ID Verification URL: https://api.gullin.io/juM8A43L9GZ7/users/idverification/' + str(id_verification.id) + '/change/'
			}
			send_email(['team@gullin.io'], 'A KYC Request Needs Manual Review (Stage 4)', 'gullin_team_notification', ctx)

			# Update ID verification instance
			id_verification.processed = True
			id_verification.note = res
			id_verification.state = res['state']
			id_verification.save()

			# Add log
			log.append('Stage 4, State R')

		elif res['state'] == 'D':
			# Send an email to user to inform that the KYC is rejected
			ctx = {
				'user_full_name': investor.full_name,
				'user_email'    : user.email
			}
			send_email([user.email], 'Gullin - ID Verification Failed', 'kyc_failed', ctx)

			# Update ID verification instance
			id_verification.processed = True
			id_verification.note = res
			id_verification.state = res['state']
			id_verification.save()

			# Reset User level
			investor.verification_level = 2
			investor.save()

			# Add log
			log.append('Stage 4, State D')

	# Get all stage 1 not finalized verifications
	verifications = IDVerification.objects.filter(processed=False, stage=1)
	for id_verification in verifications:
		investor = id_verification.investor_user
		user = investor.user
		investor_address = investor.address.first()

		if id_verification.state == 'A':
			form_data = {
				'tid'              : id_verification.tid,

				'man'              : user.email,
				'tea'              : user.email,

				'bfn'              : investor.first_name,
				'bln'              : investor.last_name,
				'dob'              : investor.birthday.isoformat(),

				'bsn'              : (investor_address.address1 + ', ') + (investor_address.address2 if investor_address.address2 else ''),
				'bc'               : investor_address.city,
				'bs'               : investor_address.state,
				'bz'               : investor_address.zipcode,
				'bco'              : country_utils.get_ISO3166_code_by_country_name(investor_address.country),

				'docType'          : id_verification.official_id_type,
				'docCountry'       : country_utils.get_ISO3166_code_by_country_name(investor.nationality),
				'scanData'         : id_verification.official_id_front_base64,
				'backsideImageData': id_verification.official_id_back_base64 if id_verification.official_id_back_base64 else '',
				'faceImages'       : [
					id_verification.user_holding_official_id_base64,
				],

				'ip'               : user.last_login_ip,
				'phn'              : user.phone_country_code + user.phone,

				'stage'            : 4,
			}
			requests.request('POST', settings.IDENTITY_MIND_API, auth=('gullin', settings.IDENTITY_MIND_KEY), json=form_data)

			id_verification.stage = 4
			id_verification.state = ''
			id_verification.official_id_front_base64 = ''
			id_verification.official_id_back_base64 = ''
			id_verification.user_holding_official_id_base64 = ''
			id_verification.save()

			# Add log
			log.append('Stage 1, State A')

		elif id_verification.state == 'R':
			id_verification.processed = True
			id_verification.save()

			# Send an email to team to inform that a kyc needs manual review
			ctx = {
				'title'  : 'A KYC Request Needs Manual Review (Stage 1)',
				'content': 'IdentityMind Transaction ID: ' + id_verification.tid + '\n' +
				           'ID Verification URL: https://api.gullin.io/juM8A43L9GZ7/users/idverification/' + str(id_verification.id) + '/change/'
			}
			send_email(['team@gullin.io'], 'A KYC Request Needs Manual Review', 'gullin_team_notification', ctx)

			# Add log
			log.append('Stage 1, State R')

		elif id_verification.state == 'D':
			# If the verification is denied, send email to notice user their id verification failed
			id_verification.processed = True
			id_verification.save()

			# Send an email to user to inform that the KYC is rejected
			ctx = {
				'user_full_name': investor.full_name,
				'user_email'    : user.email
			}
			send_email([user.email], 'Gullin - ID Verification Failed', 'kyc_failed', ctx)

			# Reset User level
			investor.verification_level = 2
			investor.save()

			# Add log
			log.append('Stage 1, State R')

	return log
