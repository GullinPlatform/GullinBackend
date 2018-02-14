from django.db import models

from Gullin.utils.upload_dir import company_icon_dir, company_member_avatar_dir


class Company(models.Model):
	"""
	Company Model
	Contains company basic info, social media info, etc.
	"""
	# Company Info
	name = models.CharField(max_length=50, unique=True)
	logo = models.ImageField(upload_to=company_icon_dir, null=True)
	display_img = models.ImageField(upload_to=company_icon_dir, null=True)
	short_description = models.CharField(max_length=150)
	website = models.URLField(max_length=150)

	# Project Description
	description = models.TextField(null=True)

	# Token Detail
	token_detail = models.OneToOneField('TokenDetail', null=True, on_delete=models.PROTECT, related_name='company')

	# Team Members
	# Documents
	# Press Releases

	# Social Media
	facebook = models.URLField(max_length=150, null=True, blank=True)
	telegram = models.URLField(max_length=150, null=True, blank=True)
	slack = models.URLField(max_length=150, null=True, blank=True)
	twitter = models.URLField(max_length=150, null=True, blank=True)
	medium = models.URLField(max_length=150, null=True, blank=True)

	# Timestamp
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name = 'Company'
		verbose_name_plural = '1. Companies'

	def __str__(self):
		return self.name


class TokenDetail(models.Model):
	"""
	TokenDetail Model
	Token Detail stores all token sake (ICO) info
	"""
	ICO_TOKEN_TYPE_CHOICES = (
		(0, 'Security'),
		(1, 'Utility'),
	)
	ICO_STAGE_TYPE_CHOICES = (
		(0, 'Pre-Sale'),
		(1, 'Crowd-Sale'),
	)

	# Token Detail
	token_code = models.CharField(max_length=10)
	token_name = models.CharField(max_length=140)
	token_logo = models.ImageField(upload_to=company_icon_dir, null=True, blank=True)
	erc20_compliant = models.BooleanField(default=True)

	# ICO Time
	start_datetime = models.DateTimeField(null=True, blank=True)
	end_datetime = models.DateTimeField(null=True, blank=True)
	is_finished = models.BooleanField(default=False)

	# ICO Type
	ico_token_type = models.IntegerField(choices=ICO_TOKEN_TYPE_CHOICES, null=True, blank=True)
	ico_stage_type = models.IntegerField(choices=ICO_STAGE_TYPE_CHOICES, null=True, blank=True)

	# Tokenomics
	price = models.FloatField(null=True, blank=True)
	total_token_supply = models.IntegerField(null=True, blank=True)

	soft_market_cap = models.FloatField(null=True, blank=True)
	hard_market_cap = models.FloatField(null=True, blank=True)
	market_cap_unit = models.CharField(max_length=10, null=True, blank=True)

	token_distribution = models.TextField(null=True, blank=True)

	# Investment Info
	threshold = models.FloatField(null=True, blank=True)
	restrictions = models.TextField(null=True, blank=True)
	bonus = models.TextField(null=True, blank=True)
	restricted_country_list = models.TextField(default='[]')

	# Smart Contract Info
	crowd_sale_contract_address = models.CharField(max_length=200, null=True, blank=True)
	token_address = models.CharField(max_length=200, null=True, blank=True)
	decimals = models.IntegerField(null=True, blank=True)

	# Timestamp
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.token_code

	class Meta:
		verbose_name_plural = '5. Token Details'


# def ico_percentage(self):
# 	return float(self.token_sold / self.total_token_supply) * 100


class PressRelease(models.Model):
	"""
	Press Release Model
	Press Release is companies updates, should only submitted by CompanyUsers or admin user
	"""
	# Company
	company = models.ForeignKey('Company', related_name='press_releases', on_delete=models.PROTECT)

	# content
	title = models.CharField(max_length=200)
	brief = models.CharField(max_length=200, null=True, blank=True)
	url = models.URLField(null=True, blank=True)

	# Timestamp
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.company.name + ' ' + self.title

	class Meta:
		verbose_name_plural = '4. Company Press Peleases'


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
	facebook = models.URLField(null=True, blank=True)
	linkedin = models.URLField(null=True, blank=True)
	website = models.URLField(null=True, blank=True)

	# Timestamp
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.company.name + ' ' + self.full_name

	@property
	def full_name(self):
		return self.first_name + ' ' + self.last_name

	class Meta:
		verbose_name_plural = '2. Company Members'


class Document(models.Model):
	# Company
	company = models.ForeignKey('Company', related_name='documents', on_delete=models.PROTECT)

	# PressRelease
	title = models.CharField(max_length=200, null=True, blank=True)
	url = models.URLField(null=True, blank=True)

	# Timestamp
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.company.name + ' ' + self.title

	class Meta:
		verbose_name_plural = '3. Company Documents'