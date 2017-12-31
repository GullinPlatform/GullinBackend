from django.utils import timezone

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser

from Gullin.utils.rest_framework_jwt.serializers import JSONWebTokenSerializer, RefreshJSONWebTokenSerializer
from Gullin.utils.rest_framework_jwt.settings import api_settings
from Gullin.utils.rest_framework_jwt.utils import jwt_return_auth_token

from Gullin.utils.get_client_ip import get_client_ip

from .serializers import CreateUserSerializer
from .models import User, InvestorUser


# Create your views here.

class UserAuthViewSet(viewsets.ViewSet):
	"""
	The viewset for user authentication, includes sign_up, log_in, log_out, and verification
	"""
	parser_classes = (MultiPartParser, FormParser, JSONParser)
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
		                                       last_name=request.data.get('last_time'))
		user.investor = investor
		user.save()

		# All InvestorUser has a insite wallet,
		# so we should create a Wallet and bind to new created InvestorUser
		# TODO

		# Return jwt token 
		return jwt_return_auth_token(user)

	def log_in(self, request):
		serializer = JSONWebTokenSerializer(data=request.data)

		if serializer.is_valid():
			user = serializer.object.get('user') or request.user
			token = serializer.object.get('token')

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

	def verify_phone(self):
		pass

	def verify_email(self):
		pass

	def resend_code(self):
		pass
