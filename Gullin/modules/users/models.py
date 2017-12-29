from django.db import models
from django.core.mail import send_mail
from datetime import timedelta

from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager

from Gullin.utils.upload_dir import user_avatar_dir, official_id_dir

from django.utils import timezone


class UserManager(BaseUserManager):
	use_in_migrations = True

	def _create_user(self, email, password, **extra_fields):
		"""
		Create and save a user with the given username, email, and password.
		"""
		if not email:
			raise ValueError('The given username must be set')

		email = self.normalize_email(email)
		user = self.model(email=email, **extra_fields)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_user(self, email=None, password=None, **extra_fields):
		extra_fields.setdefault('is_staff', False)
		extra_fields.setdefault('is_superuser', False)
		return self._create_user(email, password, **extra_fields)

	def create_superuser(self, email, password, **extra_fields):
		extra_fields.setdefault('is_staff', True)
		extra_fields.setdefault('is_superuser', True)

		if extra_fields.get('is_staff') is not True:
			raise ValueError('Superuser must have is_staff=True.')
		if extra_fields.get('is_superuser') is not True:
			raise ValueError('Superuser must have is_superuser=True.')

		return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
	"""
	Basic Users Model.
	"""

	# User Login
	email = models.EmailField(unique=True, blank=True,
	                          error_messages={'unique': "A user with that email already exists."})
	phone_prefix = models.CharField(max_length=30, null=True, blank=True)
	phone = models.CharField(max_length=30, unique=True, null=True, blank=True,
	                         error_messages={'unique': "A user with that phone already exists."})

	# Security
	last_login = models.DateTimeField(auto_now_add=True)
	last_login_ip = models.GenericIPAddressField(null=True, blank=True)
	TOTP_enabled = models.BooleanField(default=False)

	# Permissions
	is_investor = models.BooleanField(
		default=True,
		help_text='Designates whether this user is investor.'
	)
	is_company = models.BooleanField(
		default=False,
		help_text='Designates whether this user is company.'
	)
	is_analyst = models.BooleanField(
		default=False,
		help_text='Designates whether this user is analyst.'
	)
	is_staff = models.BooleanField(
		default=False,
		help_text='Designates whether the user can log into this admin site.'
	)
	is_active = models.BooleanField(
		default=True,
		help_text='Designates whether this user should be treated as active. '
		          'Unselect this instead of deleting accounts.'
	)

	# TimeStamp
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	# Settings
	USERNAME_FIELD = 'email'
	objects = UserManager()

	class Meta:
		verbose_name = 'Base User'
		verbose_name_plural = 'Base Users'
		ordering = ['-created']

	def __str__(self):
		return self.email

	def update_last_login(self):
		self.last_login = timezone.now()
		self.save(update_fields=['last_login'])

	def email_user(self, subject, message, from_email=None, **kwargs):
		"""Send an email to this user."""
		send_mail(subject, message, from_email, [self.email], **kwargs)

	def sms_user(self, subject, message, from_email=None, **kwargs):
		"""Send an sms message to this user."""
		# TODO
		pass


class InvestorUser(models.Model):
	"""
	Investor Users are able to invest in ICOs, trade ICO Tokens.
	All users registered from frontend should be investor users.
	"""
	LEVEL_CHOICES = (
		(-1, 'Not Verified'),  # Not Verified
		(0, 'LEVEL 0'),  # Email Verified
		(1, 'LEVEL 1'),  # Phone Verified
		(2, 'LEVEL 2'),  # ID Verified US Citizen
		(3, 'LEVEL 3'),  # ID Verified non-US Citizen or Accredited Investor
	)

	# Link to User Model
	user = models.OneToOneField('User', related_name='investor_user', on_delete=models.PROTECT)

	# User Info
	avatar = models.ImageField(upload_to=user_avatar_dir, default='avatars/default.jpg', null=True, blank=True)
	first_name = models.CharField(max_length=30, null=True, blank=True)
	last_name = models.CharField(max_length=50, null=True, blank=True)
	nationality = models.CharField(max_length=20, null=True, blank=True)

	# Verification
	verification_level = models.IntegerField(choices=LEVEL_CHOICES, default=-1)
	id_verification = models.OneToOneField('IDVerification', related_name='investor_user', on_delete=models.PROTECT)
	accredited_investor_verification = models.OneToOneField('InvestorVerification', related_name='investor_user', on_delete=models.PROTECT)

	# TimeStamp
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name = 'Investor'
		verbose_name_plural = 'Subusers - Investor'

	def __str__(self):
		return self.full_name

	@property
	def full_name(self):
		return self.first_name + ' ' + self.last_name


class CompanyUser(models.Model):
	"""
	Company Users are able to upload press releases, check company profile.
	Company Users can only be added by site admins.
	"""
	# Link to User Model
	user = models.OneToOneField('User', related_name='company_user', on_delete=models.PROTECT)

	# Link to Company Model
	company = models.OneToOneField('companies.Company', related_name='user', on_delete=models.PROTECT, null=True)

	# TimeStamp
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name = 'Company User'
		verbose_name_plural = 'Subusers - Company User'

	def __str__(self):
		return self.company.name


class AnalystUser(models.Model):
	"""
	Analyst Users are able to submit analyses to ICOs or companies .
	Analyst Users can only be added by site admins.
	"""
	ANALYST_TYPE_CHOICES = (
		(0, 'Professional'),
		(1, 'Regular')
	)

	# Link to User Model
	user = models.OneToOneField('User', related_name='analyst_user', on_delete=models.PROTECT)

	# User Info
	avatar = models.ImageField(upload_to=user_avatar_dir, default='avatars/default.jpg', null=True, blank=True)
	first_name = models.CharField(max_length=30, null=True, blank=True)
	last_name = models.CharField(max_length=50, null=True, blank=True)

	# Analyst Info
	analyst_type = models.IntegerField(choices=ANALYST_TYPE_CHOICES, default=1)

	# TimeStamp
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name = 'Analyst'
		verbose_name_plural = 'Subusers - Analyst'

	def __str__(self):
		return self.full_name

	@property
	def full_name(self):
		return self.first_name + ' ' + self.last_name


class IDVerification(models.Model):
	ID_TYPE_CHOICES = (('Driver License', 'Driver License'),
	                   ('Photo ID', 'Photo ID'),
	                   ('Passport', 'Passport'))

	official_id_type = models.CharField(max_length=20, choices=ID_TYPE_CHOICES)
	official_id = models.FileField(upload_to=official_id_dir, null=True, blank=True)
	nationality = models.CharField(max_length=20, null=True, blank=True)

	class Meta:
		verbose_name = 'ID Verification'
		verbose_name_plural = 'User Verification - ID'

	def __str__(self):
		return self.official_id_type


class InvestorVerification(models.Model):
	DOC_CHOICES = (('Tax Return', 'Tax Return'),
	               ('Bank Statement', 'Bank Statement'))

	doc_type = models.CharField(max_length=20, choices=DOC_CHOICES)
	doc1 = models.FileField(upload_to=official_id_dir, null=True, blank=True)
	doc2 = models.FileField(upload_to=official_id_dir, null=True, blank=True)

	class Meta:
		verbose_name = 'Accredited Investor Verification'
		verbose_name_plural = 'User Verification - Accredited Investor'

	def __str__(self):
		return self.doc_type


class VerificationToken(models.Model):
	user = models.OneToOneField('User', related_name='verification_token', on_delete=models.PROTECT)
	token = models.CharField(max_length=200)
	expire_time = models.DateTimeField(auto_now_add=True)

	@property
	def is_expired(self):
		return (timezone.now() - timedelta(hours=1)) > self.expire_time
