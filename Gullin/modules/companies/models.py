from django.db import models
from datetime import timedelta
from django.utils import timezone

from Gullin.utils.upload_dir import company_icon_dir, company_member_avatar_dir


class Company(models.Model):
	"""
	Company Model
	Contains company basic info, social media info, etc.
	"""
	# Company Info
	name = models.CharField(max_length=50, unique=True)
	logo = models.ImageField(upload_to=company_icon_dir, null=True)
	short_description = models.CharField(max_length=150)
	white_paper = models.URLField(max_length=150)
	website = models.URLField(max_length=150)

	# Token Detail
	token_detail = models.OneToOneField('TokenDetail', null=True, on_delete=models.PROTECT)

	# Press Releases

	# Project Description

	# Token Sale Plan

	# Legal Framework

	# Analysts

	# Social Media
	facebook = models.URLField(max_length=150)
	telegram = models.URLField(max_length=150)
	slack = models.URLField(max_length=150)
	twitter = models.URLField(max_length=150)
	medium = models.URLField(max_length=150)

	# Timestamp
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name = 'Company'
		verbose_name_plural = 'Companies'

	def __unicode__(self):
		return self.name


class TokenDetail(models.Model):
	"""
	TokenDetail Model
	Token Detail stores all token sake (ICO) info
	"""
	TOKEN_TYPE_CHOICES = (
		(0, 'Trading Token'),
		(1, 'Security ICO'),
	)
	ICO_TOKEN_TYPE_CHOICES = (
		(0, 'Security'),
		(1, 'Utility'),
	)
	ICO_STAGE_TYPE_CHOICES = (
		(0, 'Pre-Sale'),
		(1, 'Crowd-Sale'),
	)

	# Token Detail
	logo = models.ImageField(upload_to=company_icon_dir, null=True)
	code = models.CharField(max_length=10)
	is_finished = models.BooleanField(default=False)

	# ICO Time
	start_datetime = models.DateTimeField()
	end_datetime = models.DateTimeField()

	# ICO Type
	ico_token_type = models.IntegerField(choices=ICO_TOKEN_TYPE_CHOICES)
	ico_stage_type = models.IntegerField(choices=ICO_STAGE_TYPE_CHOICES)

	# Tokenomics
	init_price = models.FloatField()
	current_price = models.FloatField()
	total_token_supply = models.IntegerField()
	token_sold = models.FloatField()

	soft_market_cap = models.FloatField()
	hard_market_cap = models.FloatField()
	market_cap_unit = models.CharField(max_length=10)

	# Wallet Address
	wallet_address = models.CharField(max_length=200)

	# Timestamp
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.code

	def ico_percentage(self):
		return float(self.token_sold / self.total_token_supply) * 100


class PressRelease(models.Model):
	"""
	Press Release Model
	Press Release is companies updates, should only submitted by CompanyUsers or admin user
	"""
	# Company
	company = models.ForeignKey('Company', related_name='press_releases', on_delete=models.PROTECT)

	# content
	title = models.CharField(max_length=200)
	content = models.TextField(null=True, blank=True)
	url = models.URLField(null=True, blank=True)

	# Timestamp
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.company.name + ' ' + self.title


class CompanyMember(models.Model):
	"""
	Company Member Model
	contains company member info
	"""
	MEMBER_TYPE_CHOICES = (
		(0, 'Advisor'),
		(1, 'Member'),
	)

	# Company
	company = models.ForeignKey('Company', related_name='members', on_delete=models.PROTECT)

	# Member info
	avatar = models.ImageField(upload_to=company_member_avatar_dir, default='avatars/default.jpg', null=True, blank=True)
	first_name = models.CharField(max_length=30)
	last_name = models.CharField(max_length=50)
	title = models.CharField(max_length=200, null=True, blank=True)
	description = models.CharField(max_length=200, null=True, blank=True)
	member_type = models.IntegerField(default=1, choices=MEMBER_TYPE_CHOICES)

	# Social Media
	facebook = models.URLField()
	linkedin = models.URLField()

	# Timestamp
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.company.name + ' ' + self.full_name

	@property
	def full_name(self):
		return self.first_name + ' ' + self.last_name
