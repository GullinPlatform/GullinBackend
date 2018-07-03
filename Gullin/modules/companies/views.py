from django.utils import timezone
from django.core.paginator import Paginator

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import  AllowAny, IsAuthenticated
from rest_framework.parsers import FormParser, JSONParser

from .serializers import ListCompanySerializer, FullCompanySerializer, FullPressReleaseSerializer, FullWhitelistSerializer
from .models import Company, PressRelease, Whitelist


class CompanyViewSet(viewsets.ViewSet):
	"""
	The viewset for company module
	"""
	parser_classes = (FormParser, JSONParser)
	permission_classes = (AllowAny,)

	def list(self, request, list_type):
		companies = Company.objects.filter(published=True)
		if list_type == 'active':
			serializer = ListCompanySerializer(
				companies.filter(token_detail__end_datetime__gt=timezone.now(), token_detail__start_datetime__lt=timezone.now()).order_by('token_detail__end_datetime'),
				many=True)
		elif list_type == 'coming':
			serializer = ListCompanySerializer(
				companies.filter(token_detail__start_datetime__gt=timezone.now()).order_by('token_detail__end_datetime'),
				many=True)
		elif list_type == 'all':
			serializer = ListCompanySerializer(
				companies.order_by('token_detail__end_datetime'),
				many=True)
		else:
			serializer = ListCompanySerializer(
				companies.filter(token_detail__end_datetime__gt=timezone.now()).order_by('token_detail__end_datetime'),
				many=True)
		return Response(serializer.data)

	def detail(self, request, id):
		try:
			company = Company.objects.filter(id=id).first()
			if company:
				serializer = FullCompanySerializer(company)
				return Response(serializer.data)
		except ValueError:
			if Company.objects.filter(name=id):
				company = Company.objects.get(name=id)
				serializer = FullCompanySerializer(company)
				return Response(serializer.data)
			elif Company.objects.filter(token_detail__token_code=id):
				company = Company.objects.get(token_detail__token_code=id)
				serializer = FullCompanySerializer(company)
				return Response(serializer.data)

		return Response(status=status.HTTP_404_NOT_FOUND)

	def press_releases(self, request):
		# TODO: Pagination
		press_releases = PressRelease.objects.all()
		serializer = FullPressReleaseSerializer(press_releases, many=True)
		return Response(serializer.data)


class CompanyPortalViewSet(viewsets.ViewSet):
	parser_classes = (FormParser, JSONParser)
	permission_classes = (IsAuthenticated,)

	def whitelist(self, request):
		if request.user.is_company_user:
			if request.GET.get('category') == 'name':
				if request.GET.get('direction') == 'descending':
					whitelist = Whitelist.objects.filter(company=request.user.company_user.company.id).order_by('-investor__last_name')
				else:
					whitelist = Whitelist.objects.filter(company=request.user.company_user.company.id).order_by(
						'investor__last_name')
			elif request.GET.get('category') == 'nationality':
				if request.GET.get('direction') == 'descending':
					whitelist = Whitelist.objects.filter(company=request.user.company_user.company.id).order_by('-investor__nationality')
				else:
					whitelist = Whitelist.objects.filter(company=request.user.company_user.company.id).order_by(
						'investor__nationality')
			elif request.GET.get('category') == 'pledge_amount':
				if request.GET.get('direction') == 'descending':
					whitelist = Whitelist.objects.filter(company=request.user.company_user.company.id).order_by('-pledge_amount')
				else:
					whitelist = Whitelist.objects.filter(company=request.user.company_user.company.id).order_by(
						'pledge_amount')
			elif request.GET.get('category') == 'joined_whitelist':
				if request.GET.get('direction') == 'descending':
					whitelist = Whitelist.objects.filter(company=request.user.company_user.company.id).order_by('-joined_whitelist_timestamp')
				else:
					whitelist = Whitelist.objects.filter(company=request.user.company_user.company.id).order_by(
						'joined_whitelist_timestamp')
			paginator = Paginator(whitelist, 50)
			page_number = request.GET.get('page_number')
			whitelist = paginator.get_page(page_number)
			serializer = FullWhitelistSerializer(whitelist, many=True)
			return Response(serializer.data)