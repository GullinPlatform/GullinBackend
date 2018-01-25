from django.utils import timezone

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser

from Gullin.utils.rest_framework_jwt.serializers import JSONWebTokenSerializer, RefreshJSONWebTokenSerializer
from Gullin.utils.rest_framework_jwt.settings import api_settings
from Gullin.utils.rest_framework_jwt.utils import jwt_return_auth_token

from Gullin.utils.get_client_ip import get_client_ip
from Gullin.utils.validate_country_code import is_valid_country, get_code_by_country_name
from Gullin.utils.send.email import send_email
from Gullin.utils.send.sms import send_sms

from .serializers import CreateUserSerializer, FullIDVerificationSerializer, FullInvestorUserSerializer
from .models import InvestorUser
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
			'full_name'        : investor.full_name,
			'verification_code': verification_code.code
		}
		send_email([user.email], 'Gullin - Verification Code', 'send_email_verification_code', ctx)

		# Return jwt token
		return jwt_return_auth_token(user)

	def log_in(self, request):
		serializer = JSONWebTokenSerializer(data=request.data)

		if serializer.is_valid():
			user = serializer.object.get('user') or request.user
			token = serializer.object.get('token')
			# TODO: 2 factor auth need to be implemented

			# Update user last login timestamp
			user.update_last_login()

			# Update user last login IP
			user.update_last_login_ip(get_client_ip(request))

			jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER
			response_data = jwt_response_payload_handler(token, user, request)

			if api_settings.JWT_AUTH_COOKIE:
				response = Response()
				response.set_cookie(api_settings.JWT_AUTH_COOKIE,
				                    response_data['token'],
				                    expires=(timezone.now() + api_settings.JWT_EXPIRATION_DELTA),
				                    httponly=True)
			else:
				response = Response(response_data)

			return response
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def log_out(self, request):
		response = Response()
		response.delete_cookie('gullin_jwt')
		return response

	def refresh(self, request):
		data = request.data.copy()
		if api_settings.JWT_AUTH_COOKIE:
			data['token'] = request.COOKIES.get(api_settings.JWT_AUTH_COOKIE)

		serializer = RefreshJSONWebTokenSerializer(data=data)

		if serializer.is_valid():
			user = serializer.object.get('user') or request.user
			token = serializer.object.get('token')

			jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER
			response_data = jwt_response_payload_handler(token, user, request)

			if api_settings.JWT_AUTH_COOKIE:
				response = Response()
				response.set_cookie(api_settings.JWT_AUTH_COOKIE,
				                    response_data['token'],
				                    expires=(timezone.now() + api_settings.JWT_EXPIRATION_DELTA),
				                    httponly=True)
			else:
				response = Response(response_data)

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
		if not verification_code.is_expired and request.data.get('verification_code') == verification_code:
			# Update user verification level
			investor_user.verification_level = 0
			investor_user.save()

			# Expire verification code
			verification_code.expire()

			return Response(status=status.HTTP_200_OK)
		else:
			return Response({'error': 'Verification failed, please try again or request another code'},
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
				user.save()

				# Do an arbitrary assumption of user's nationality based on phone number
				investor_user.nationality = country_name
				investor_user.investor.save()

				# Send SMS to user
				verification_code.refresh()
				phone_num = user.phone_country_code + user.phone
				msg = 'Verification Code: ' + verification_code.code + '\n Valid in 5 minutes.'
				send_sms(phone_num, msg)

				return Response(status=status.HTTP_200_OK)
			else:
				return Response({'error': 'Phone number invalid, please check again'},
				                status=status.HTTP_400_BAD_REQUEST)

		# Verify user phone number
		elif request.method == 'PATCH':
			investor_user = request.user.investor
			verification_code = request.user.verification_code
			if not verification_code.is_expired and request.data.get('verification_code') == verification_code:
				# Update user verification level
				investor_user.verification_level = 1
				investor_user.save()

				# Expire verification code
				verification_code.expire()

				return Response(status=status.HTTP_200_OK)
			else:
				return Response({'error': 'Verification failed, please try again or request another code'},
				                status=status.HTTP_400_BAD_REQUEST)

	def resend_code(self, request):
		if request.data.get('email'):
			verification_code = request.user.verification_code
			verification_code.refresh()
			ctx = {
				'full_name'        : request.user.investor.full_name,
				'verification_code': verification_code.code
			}
			send_email([request.user.email], 'Gullin - Verification Code', 'send_email_verification_code', ctx)
			return Response(status=status.HTTP_200_OK)

		elif request.data.get('sms'):
			verification_code = request.user.verification_code
			verification_code.refresh()

			phone_num = request.user.phone_country_code + request.user.phone
			msg = 'Gullin Verification Code: ' + verification_code.code + '\n Valid in 5 minutes.'
			send_sms(phone_num, msg)

			return Response(status=status.HTTP_200_OK)

	def save_wallet_address(self, request):
		user_wallet = request.user.investor.wallet
		if user_wallet.eth_address:
			return Response(status=status.HTTP_403_FORBIDDEN)
		else:
			user_wallet.eth_address = request.data.get('public_address')
			user_wallet.save()
			return Response(status=status.HTTP_400_BAD_REQUEST)

	def upload_id(self, request):
		# request.data needs 'official_id_type', 'official_id_back', 'official_id_front', 'nationality'
		serializer = FullIDVerificationSerializer(data=request.data)
		if serializer.is_valid():
			id_verification = serializer.save()
			request.user.investor.id_verification = id_verification
			request.user.investor.save()

			return Response(status=status.HTTP_201_CREATED)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ViewSet):
	parser_classes = (MultiPartParser, FormParser, JSONParser)
	permission_classes = (IsAuthenticated,)

	def me(self, request):
		if request.method == 'GET':
			# Retrieve self
			if request.user.is_investor:
				serializer = FullInvestorUserSerializer(request.user.investor)
			elif request.user.is_company_user:
				# TODO
				pass
			elif request.user.is_analyst:
				# TODO
				pass
			return Response(serializer.data)
		elif request.method == 'PATCH':
			# Update self
			pass

	def accredited_investor_verification(self, request):
		pass
