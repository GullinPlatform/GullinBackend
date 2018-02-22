from django.urls import path

from .views import UserAuthViewSet, UserSignUpFollowUpViewSet, UserViewSet, send_kyc_email

user_login = UserAuthViewSet.as_view({
	'post' : 'log_in',
	'patch': 'log_in'
})

user_logout = UserAuthViewSet.as_view({
	'post': 'log_out'
})

user_signup = UserAuthViewSet.as_view({
	'post': 'sign_up'
})

user_refresh = UserAuthViewSet.as_view({
	'post': 'refresh'
})

user_wallet_address = UserSignUpFollowUpViewSet.as_view({
	'post': 'save_wallet_address'
})

user_verify_email = UserSignUpFollowUpViewSet.as_view({
	'patch': 'verify_email'
})

user_verify_phone = UserSignUpFollowUpViewSet.as_view({
	'post' : 'verify_phone',
	'patch': 'verify_phone'
})

user_resend_verification_code = UserSignUpFollowUpViewSet.as_view({
	'post': 'resend_code'
})

user_me = UserViewSet.as_view({
	'get'  : 'me',
	'patch': 'me',
})

user_id_verification = UserViewSet.as_view({
	'post': 'id_verification'
})

urlpatterns = [
	path('auth/signup/', user_signup, name='user_signup'),
	path('auth/login/', user_login, name='user_login'),
	path('auth/refresh/', user_refresh, name='user_refresh'),
	path('auth/logout/', user_logout, name='user_logout'),

	path('followup/email/', user_verify_email, name='user_verify_email'),
	path('followup/phone/', user_verify_phone, name='user_verify_phone'),
	path('followup/resend/', user_resend_verification_code, name='user_resend_verification_code'),
	path('followup/wallet_address/', user_wallet_address, name='user_wallet_address'),

	path('verify/upload_id/', user_id_verification, name='user_id_verification'),

	path('me/', user_me, name='user_me'),

	path('send_kyc_email/<type>/<email>', send_kyc_email)
]
