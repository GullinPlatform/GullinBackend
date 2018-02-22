from django.utils import timezone
from django.db.utils import IntegrityError
from django.contrib.gis.geoip2 import GeoIP2

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser

from Gullin.utils.rest_framework_jwt.serializers import JSONWebTokenSerializer, RefreshJSONWebTokenSerializer
from Gullin.utils.rest_framework_jwt.settings import api_settings as jwt_settings

from Gullin.utils.get_client_ip import get_client_ip
from Gullin.utils.validate_country_code import is_valid_country, get_code_by_country_name
from Gullin.utils.send.email import send_email
from Gullin.utils.send.sms import send_sms

from .serializers import CreateUserSerializer, FullIDVerificationSerializer, FullInvestorUserSerializer
from .models import InvestorUser, User, InvestorUserAddress, UserLog
from ..wallets.models import Wallet


class UserAuthViewSet(viewsets.ViewSet):
	"""
	The viewset for user authentication, includes sign_up, log_in, log_out, and verification
	"""
	parser_classes = (FormParser, JSONParser)
	permission_classes = (AllowAny,)

	def sign_up(self, request):
		# Get user login IP and add to data
		data = request.data.copy()
		data['last_login_ip'] = get_client_ip(request)

		# Create user instance using serializer
		serializer = CreateUserSerializer(data=data)
		serializer.is_valid(raise_exception=True)
		user = serializer.save()

		# All User created through this method is investor,
		# so we should create a InvestorUser instance and bind to new created User
		investor = InvestorUser.objects.create(first_name=request.data.get('first_name'),
		                                       last_name=request.data.get('last_name'))
		user.investor = investor
		user.save()

		# All InvestorUser has a insite wallet,
		# so we should create a Wallet instance and bind to new created InvestorUser
		# IMPORTANT: since the public/private key pair is generated on the frontend, it will be stored to database later
		wallet = Wallet.objects.create(investor_user=investor)
		# Init Balance objects and add to wallet
		wallet.init_balance()

		# Send user verification email when user register
		verification_code = user.verification_code
		verification_code.refresh()
		ctx = {
			'user_full_name'   : investor.full_name,
			'verification_code': verification_code.code,
			'user_email'       : user.email
		}
		send_email([user.email], 'Gullin - Welcome! Please Verify Your Email', 'welcome_and_email_verification', ctx)

		# Get user auth token
		payload = jwt_settings.JWT_PAYLOAD_HANDLER(user)
		token = jwt_settings.JWT_ENCODE_HANDLER(payload)

		# Construct response object to set cookie
		serializer = FullInvestorUserSerializer(user.investor)
		response = Response(serializer.data, status=status.HTTP_201_CREATED)
		response.set_cookie(jwt_settings.JWT_AUTH_COOKIE,
		                    token,
		                    expires=(timezone.now() + jwt_settings.JWT_EXPIRATION_DELTA),
		                    httponly=True)
		return response

	def log_in(self, request):
		# Login Attempt
		if request.method == 'POST':
			# Try login
			serializer = JSONWebTokenSerializer(data=request.data)
			# If login successful
			if serializer.is_valid():
				# get user instance and ip
				user = serializer.object.get('user')
				auth_token = serializer.object.get('token')
				user_ip = get_client_ip(request)

				# if user logged in form a old ip
				if user_ip == user.last_login_ip:
					# Update user last login timestamp and last login IP
					user.update_last_login()
					user.update_last_login_ip(user_ip)

					# Generate Log
					UserLog.objects.create(user_id=user.id,
					                       ip=user_ip,
					                       action='Login Successful',
					                       device=request.META['HTTP_USER_AGENT'])
					# Generate Response
					# Add user to the response data
					serializer = FullInvestorUserSerializer(user.investor)
					response_data = serializer.data
					response_data['data'] = 'success'
					response = Response(response_data, status=status.HTTP_200_OK)
					# Add cookie to the response data
					response.set_cookie(jwt_settings.JWT_AUTH_COOKIE,
					                    auth_token,
					                    expires=(timezone.now() + jwt_settings.JWT_EXPIRATION_DELTA),
					                    httponly=True)
					return response

				# else go to 2 factor auth
				# Save user and token to session
				request.session['user_id'] = user.id
				request.session['auth_token'] = serializer.object.get('token')

				# Start 2 factor auth code
				# If user not enabled TOTP
				if not user.TOTP_enabled:
					# Make sure user has phone number
					if user.phone:
						# Refresh code
						user.verification_code.refresh()
						# Send sms
						phone_num = user.phone_country_code + user.phone
						send_sms(phone_num,
						         'Verification Code: ' + user.verification_code.code + '\nInvalid in 5 minutes.')
						msg = {'data': 'We have sent a verification code to your phone, please verify.'}
					# Else send 2-factor to users email
					else:
						# Refresh code
						user.verification_code.refresh()
						# Send email
						verification_code = user.verification_code
						verification_code.refresh()
						ctx = {
							'user_full_name'   : user.investor.full_name,
							'verification_code': verification_code.code,
							'user_email'       : user.email
						}
						send_email([user.email], 'Gullin - Welcome! Please Verify Your Email', 'welcome_and_email_verification', ctx)

						msg = {'data': 'We have sent a verification code to your email, please verify.'}
				# If user enabled TOTP
				else:
					# TODO: work with TOTP clients
					msg = {'data': 'Please verify using your 2 factor authenticator.'}
					pass

				# Generate Log
				UserLog.objects.create(user_id=user.id,
				                       ip=get_client_ip(request),
				                       action='Login Successful (Need 2 Factor Auth)',
				                       device=request.META['HTTP_USER_AGENT'])
				# Send Warning Email
				g = GeoIP2()
				try:
					city = g.city(user_ip)
					location = city.get('city') + ', ' + city.get('country_name')
				except:
					location = 'Unknown'
				ctx = {
					'user_full_name': user.investor.full_name,
					'user_email'    : user.email,
					'user_ip'       : user_ip,
					'user_location' : location,
					'user_device'   : request.META['HTTP_USER_AGENT'],
				}
				send_email([user.email], 'Gullin - Login from a different IP', 'different_ip_login_notice', ctx)

				return Response(msg, status=status.HTTP_200_OK)
			else:
				return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

		# Verify 2 Factor code
		elif request.method == 'PATCH':
			# check session
			if request.session.get('user_id') and request.session.get('auth_token'):
				# retrieve data from session
				user = User.objects.get(id=request.session['user_id'])
				token = request.session['auth_token']

				# Check verifications code
				# If user not enabled TOTP
				if not user.TOTP_enabled:
					verification_code = user.verification_code
					# Check If code is valid
					if verification_code.is_expired:
						return Response({'error': 'Verification code expired, please request another code.'},
						                status=status.HTTP_400_BAD_REQUEST)
					if not (request.data.get('verification_code') == verification_code.code):
						return Response({'error': 'Verification code doesn\'t match, please try again or request another code.'},
						                status=status.HTTP_400_BAD_REQUEST)
					# Verification code is valid, so expire verification code
					verification_code.expire()

				# If user enabled TOTP
				else:
					# TODO: work with TOTP clients
					pass

				# Code is valid

				# Clear session
				request.session.clear()
				user_ip = get_client_ip(request)

				# Update user last login timestamp and last login IP
				user.update_last_login()
				user.update_last_login_ip(user_ip)

				# Generate Log
				UserLog.objects.create(user_id=user.id,
				                       ip=user_ip,
				                       action='2 Factor Auth Successful',
				                       device=request.META['HTTP_USER_AGENT'])

				# Generate Response
				# Add user to the response data
				serializer = FullInvestorUserSerializer(user.investor)
				response = Response(serializer.data, status=status.HTTP_200_OK)
				# Add cookie to the response data
				response.set_cookie(jwt_settings.JWT_AUTH_COOKIE,
				                    token,
				                    expires=(timezone.now() + jwt_settings.JWT_EXPIRATION_DELTA),
				                    httponly=True)
				return response
			else:
				return Response({'error': 'You have to login first!'}, status=status.HTTP_400_BAD_REQUEST)

	def log_out(self, request):
		response = Response()
		response.delete_cookie('gullin_jwt')
		return response

	def refresh(self, request):
		data = request.data.copy()
		data['token'] = request.COOKIES.get(jwt_settings.JWT_AUTH_COOKIE)

		serializer = RefreshJSONWebTokenSerializer(data=data)

		if serializer.is_valid():
			user = serializer.object.get('user') or request.user
			token = serializer.object.get('token')

			# Generate Response
			# Add user to the response data
			serializer = FullInvestorUserSerializer(user.investor)
			response = Response(serializer.data, status=status.HTTP_200_OK)
			# Add cookie to the response data
			response.set_cookie(jwt_settings.JWT_AUTH_COOKIE,
			                    token,
			                    expires=(timezone.now() + jwt_settings.JWT_EXPIRATION_DELTA),
			                    httponly=True)
			return response

		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserSignUpFollowUpViewSet(viewsets.ViewSet):
	"""
	The viewset for user sign up follow-up, includes phone verification, email verification and id uploading
	"""
	parser_classes = (MultiPartParser, FormParser, JSONParser)
	permission_classes = (IsAuthenticated,)

	def verify_email(self, request):
		# Verify user email
		investor_user = request.user.investor
		verification_code = request.user.verification_code
		if request.data.get('verification_code') == verification_code.code:
			if not verification_code.is_expired:
				# Update user verification level
				investor_user.verification_level = 0
				investor_user.save()

				# Expire verification code
				verification_code.expire()

				return Response(status=status.HTTP_200_OK)
			else:
				return Response({'error': 'Verification code expired, please request another code.'},
				                status=status.HTTP_400_BAD_REQUEST)
		else:
			return Response({'error': 'Verification code doesn\'t match, please try again or request another code.'},
			                status=status.HTTP_400_BAD_REQUEST)

	def verify_phone(self, request):
		# Add phone number for the current user and send verification code
		if request.method == 'POST':
			# request.data must contain country_name, phone
			country_name = request.data.get('country_name')
			if is_valid_country(country_name):
				# Cache
				user = request.user
				investor_user = request.user.investor
				verification_code = request.user.verification_code

				# Update phone number of user model
				user.phone_country_code = get_code_by_country_name(country_name)
				user.phone = request.data.get('phone')
				try:
					user.save()
				except IntegrityError:
					return Response({'error': 'A user with this phone number already exists.'},
					                status=status.HTTP_403_FORBIDDEN)

				# Do an arbitrary assumption of user's nationality based on phone number
				investor_user.nationality = country_name
				investor_user.save()

				# Send SMS to user
				verification_code.refresh()
				phone_num = user.phone_country_code + user.phone
				msg = 'Verification Code: ' + verification_code.code + '\nInvalid in 5 minutes.'
				send_sms(phone_num, msg)

				return Response(status=status.HTTP_200_OK)
			else:
				return Response({'error': 'Phone number invalid, please check again'},
				                status=status.HTTP_400_BAD_REQUEST)

		# Verify user phone number
		elif request.method == 'PATCH':
			investor_user = request.user.investor
			verification_code = request.user.verification_code
			if request.data.get('verification_code') == verification_code.code:
				if not verification_code.is_expired:
					# Update user verification level
					investor_user.verification_level = 1
					investor_user.save()

					# Expire verification code
					verification_code.expire()

					return Response(status=status.HTTP_200_OK)
				else:
					return Response({'error': 'Verification code expired, please request another code.'},
					                status=status.HTTP_400_BAD_REQUEST)
			else:
				return Response({'error': 'Verification code doesn\'t match, please try again or request another code.'},
				                status=status.HTTP_400_BAD_REQUEST)

	def save_wallet_address(self, request):
		investor = request.user.investor
		if investor.wallet.eth_address:
			return Response({'error': 'Your are already bound with a wallet'}, status=status.HTTP_403_FORBIDDEN)
		else:
			investor.wallet.eth_address = request.data.get('eth_address')
			investor.wallet.save()
			# Update verification level
			investor.verification_level = 2
			investor.save()
			return Response(status=status.HTTP_200_OK)


class UserViewSet(viewsets.ViewSet):
	parser_classes = (MultiPartParser, FormParser, JSONParser)
	permission_classes = (IsAuthenticated,)

	def me(self, request):
		if request.method == 'GET':
			# if request.user.is_investor:
			# 	serializer = FullInvestorUserSerializer(request.user.investor)
			# elif request.user.is_company_user:
			# 	# TODO
			# 	pass
			# elif request.user.is_analyst:
			# 	# TODO
			# 	pass

			# Retrieve self
			serializer = FullInvestorUserSerializer(request.user.investor)
			return Response(serializer.data)
		elif request.method == 'PATCH':
			# Update Address
			if request.data.get('update') == 'address':
				# Check content
				if request.user.investor.address:
					address = request.user.investor.address
					address.address1 = request.data['address1']
					address.address2 = request.data['address2']
					address.city = request.data['city']
					address.state = request.data['state']
					address.zipcode = request.data['zipcode']
					address.country = request.user.investor.nationality
					address.save()
				else:
					address = InvestorUserAddress.objects.create(address1=request.data['address1'],
					                                             address2=request.data['address2'],
					                                             city=request.data['city'],
					                                             state=request.data['state'],
					                                             zipcode=request.data['zipcode'],
					                                             country=request.user.investor.nationality)
					request.user.investor.address = address
					request.user.investor.save()
				serializer = FullInvestorUserSerializer(request.user.investor)
				return Response(serializer.data, status=status.HTTP_200_OK)

			# Update Birthday
			elif request.data.get('update') == 'name_birthday':
				investor_user = request.user.investor

				# If user ID approved
				if investor_user.verification_level >= 3:
					# User cannot change birthday and name
					return Response(status.HTTP_403_FORBIDDEN)

				if request.data.get('birthday'):
					investor_user.birthday = request.data.get('birthday')
				if request.data.get('first_name'):
					request.user.first_name = request.data.get('first_name')
				if request.data.get('last_name'):
					request.user.last_name = request.data.get('last_name')
				investor_user.save()

				serializer = FullInvestorUserSerializer(request.user.investor)
				return Response(serializer.data, status=status.HTTP_200_OK)

	def upload_id(self, request):
		# request.data needs 'official_id_type', 'official_id_back', 'official_id_front', 'nationality'
		serializer = FullIDVerificationSerializer(data=request.data)
		if serializer.is_valid():
			id_verification = serializer.save()
			investor = request.user.investor
			investor.id_verification = id_verification
			investor.verification_level = 3
			investor.save()

			return Response(status=status.HTTP_201_CREATED)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def send_verification_code(self, request):
		if request.data.get('email'):
			verification_code = request.user.verification_code
			verification_code.refresh()
			ctx = {
				'user_full_name'   : request.user.investor.full_name,
				'verification_code': verification_code.code,
				'user_email'       : request.user.email
			}
			send_email([request.user.email], 'Gullin - Verification Code', 'verification_code', ctx)
			return Response(status=status.HTTP_200_OK)

		elif request.data.get('sms'):
			verification_code = request.user.verification_code
			verification_code.refresh()

			phone_num = request.user.phone_country_code + request.user.phone
			msg = 'Gullin Verification Code: ' + verification_code.code + '\n Valid in 5 minutes.'
			send_sms(phone_num, msg)

			return Response(status=status.HTTP_200_OK)

	def accredited_investor_verification(self, request):
		pass

	def two_factor_auth(self, request):
		pass
