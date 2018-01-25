from django.urls import path

from .views import WalletViewSet

company_list = WalletViewSet.as_view({
	'get': 'list',
})

company_detail = WalletViewSet.as_view({
	'get': 'detail',
})


urlpatterns = [
	path('list/<list_type>/', company_list, name='company_list'),
	path('<int:id>/', company_detail, name='company_detail'),
]
