from django.urls import path

from .views import UserAuthViewSet

user_login = UserAuthViewSet.as_view({
	'post': 'log_in'
})

user_logout = UserAuthViewSet.as_view({
	'post': 'log_out'
})

user_signup = UserAuthViewSet.as_view({
	'post': 'sign_up'
})

urlpatterns = [
	path('login/', user_login, name='user_login'),
	path('logout/', user_logout, name='user_logout'),
	path('signup/', user_signup, name='user_signup')
]
