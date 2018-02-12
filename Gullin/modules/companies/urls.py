from django.urls import path

from .views import CompanyViewSet

company_list = CompanyViewSet.as_view({
	'get': 'list',
})

company_detail = CompanyViewSet.as_view({
	'get': 'detail',
})
company_press_releases = CompanyViewSet.as_view({
	'get': 'press_releases',
})

urlpatterns = [
	path('press_releases/', company_press_releases, name='company_press_releases'),
	path('list/<list_type>/', company_list, name='company_list'),
	path('<id>/', company_detail, name='company_detail'),
]
