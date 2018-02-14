from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group as BuiltInGroup

from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import User, InvestorUser, CompanyUser, AnalystUser, InvestorUserAddress, InvestorVerification, IDVerification, VerificationCode, UserLog
from .forms import UserCreationForm


@admin.register(User)
class UserAdmin(BaseUserAdmin):
	# Add Form Settings
	add_form = UserCreationForm
	add_fieldsets = (
		(None, {
			'classes': ('wide',),
			'fields' : ('email', 'password1', 'password2',),
		}),
	)

	# List display Settings
	list_display = ('id', 'email', 'phone', 'created', 'last_login_ip',)
	search_fields = ('email', 'phone',)
	list_filter = ('created',)
	ordering = ('created',)

	# Detail Page Settings
	fieldsets = (
		('User Info', {'fields': ('email', 'phone_country_code', 'phone', 'password',)}),
		('User Extension', {'fields': ('edit_investor',)}),
		('Permissions', {'fields': ('is_investor', 'is_company_user', 'is_analyst', 'is_active', 'is_staff',)}),
		('Security', {'fields': ('last_login', 'last_login_ip', 'TOTP_enabled',)}),
		('Timestamp', {'fields': ('created', 'updated',)}),
	)
	readonly_fields = ('created', 'updated',
	                   'last_login', 'last_login_ip', 'TOTP_enabled',
	                   'is_investor', 'is_company_user', 'is_analyst', 'is_active', 'is_staff',
	                   'edit_investor')

	def edit_investor(self, obj):
		if obj.is_investor:
			change_url = reverse('admin:users_investoruser_change', args=(obj.investor.id,))
			return mark_safe('<a href="%s">%s</a>' % (change_url, obj.investor.full_name))
		else:
			return '-'

	# def edit_company_user(self, obj):
	# 	if obj.is_company:
	# 		change_url = reverse('admin:users_companyuser_change', args=(obj.company_user.id,))
	# 		return mark_safe('<a href="%s">%s</a>' % (change_url, obj.company_user))
	# 	else:
	# 		return '-'
	#
	# def edit_analyst(self, obj):
	# 	if obj.is_analyst:
	# 		change_url = reverse('admin:users_user_change', args=(obj.analyst.id,))
	# 		return mark_safe('<a href="%s">%s</a>' % (change_url, obj.analyst.full_name))
	# 	else:
	# 		return '-'


@admin.register(InvestorUser)
class InvestorUserAdmin(admin.ModelAdmin):
	# List display Settings
	list_display = ('id', 'full_name', 'nationality', 'verification_level',)
	search_fields = ('user', 'full_name',)
	list_filter = ('verification_level', 'nationality',)
	ordering = ('created',)

	# Detail Page Settings
	fieldsets = (
		('Base User', {'fields': ('edit_user',)}),
		('User Info', {'fields': ('first_name', 'last_name', 'birthday', 'nationality', 'address',)}),
		('Verification', {'fields': ('verification_level', 'id_verification', 'accredited_investor_verification',)}),
		('Timestamp', {'fields': ('created', 'updated',)}),
	)
	readonly_fields = ('created', 'updated', 'edit_user')

	def edit_user(self, obj):
		change_url = reverse('admin:users_user_change', args=(obj.user.id,))
		return mark_safe('<a href="%s">%s</a>' % (change_url, obj.user.email))


# @admin.register(AnalystUser)
class AnalystUserAdmin(admin.ModelAdmin):
	# List display Settings
	list_display = ('id', 'full_name', 'created', 'updated',)
	search_fields = ('user', 'full_name',)
	list_filter = ('analyst_type',)
	ordering = ('created',)

	# Detail Page Settings
	fieldsets = (
		('Base User', {'fields': ('edit_user',)}),
		('User Info', {'fields': ('avatar', 'first_name', 'last_name',)}),
		('Analyst Info', {'fields': ('analyst_type',)}),
		('Timestamp', {'fields': ('created', 'updated',)}),
	)
	readonly_fields = ('created', 'updated', 'edit_user',)

	def edit_user(self, obj):
		change_url = reverse('admin:users_user_change', args=(obj.user.id,))
		return mark_safe('<a href="%s">%s</a>' % (change_url, obj.user.email))


# @admin.register(CompanyUser)
class CompanyUserAdmin(admin.ModelAdmin):
	# List display Settings
	list_display = ('id', 'user', 'created', 'updated',)
	search_fields = ('user',)
	ordering = ('created',)

	# Detail Page Settings
	fieldsets = (
		('Base User', {'fields': ('edit_user',)}),
		('Company Info', {'fields': ('company',)}),
		('Timestamp', {'fields': ('created', 'updated',)}),
	)
	readonly_fields = ('created', 'updated', 'edit_user',)

	def edit_user(self, obj):
		change_url = reverse('admin:users_user_change', args=(obj.user.id,))
		return mark_safe('<a href="%s">%s</a>' % (change_url, obj.user.email))


@admin.register(InvestorUserAddress)
class InvestorUserAddressAdmin(admin.ModelAdmin):
	# List display Settings
	list_display = ('id', 'investor_user', 'created', 'updated',)
	ordering = ('created',)

	# Detail Page Settings
	fieldsets = (
		('Base User', {'fields': ('edit_investor_user',)}),
		('Address Info', {'fields': ('address1', 'address2', 'city', 'state', 'zipcode', 'country',)}),
		('Timestamp', {'fields': ('created', 'updated',)}),
	)
	readonly_fields = ('created', 'updated', 'edit_investor_user',)

	def edit_investor_user(self, obj):
		change_url = reverse('admin:users_investoruser_change', args=(obj.investor_user.id,))
		return mark_safe('<a href="%s">%s</a>' % (change_url, obj.investor_user.full_name))


@admin.register(IDVerification)
class IDVerificationAdmin(admin.ModelAdmin):
	# List display Settings
	list_display = ('id', 'investor_user', 'official_id_type', 'created', 'updated',)
	search_fields = ('investor_user',)
	ordering = ('created',)

	# Detail Page Settings
	fieldsets = (
		('Base User', {'fields': ('edit_investor_user',)}),
		('ID Info', {'fields': ('official_id_type', 'official_id_front', 'official_id_back', 'user_holding_official_id',)}),
		('Nationality', {'fields': ('nationality',)}),
		('Verify', {'fields': ('is_verified',)}),
		# ('Action', {'fields': ('verify_identity', 'unverify_identity')}),
		('Timestamp', {'fields': ('created', 'updated',)}),
	)
	readonly_fields = ('created', 'updated', 'edit_investor_user')

	def edit_investor_user(self, obj):
		change_url = reverse('admin:users_investoruser_change', args=(obj.investor_user.id,))
		return mark_safe('<a href="%s">%s</a>' % (change_url, obj.investor_user.full_name))

	# def verify_identity(self, obj):
	# 	return obj.verify_identity()
	#
	# def unverify_identity(self, obj):
	# 	return obj.unverify_identity()


@admin.register(InvestorVerification)
class InvestorVerificationAdmin(admin.ModelAdmin):
	# user = models.OneToOneField('User', related_name='email_token', on_delete=models.PROTECT)
	# token = models.CharField(max_length=200)
	# expire_time = models.DateTimeField(auto_now_add=True)
	pass


@admin.register(VerificationCode)
class VerificationCodeAdmin(admin.ModelAdmin):
	# List display Settings
	list_display = ('user', 'code', 'expire_time', 'is_expired',)
	search_fields = ('user',)
	# list_filter = ('is_expired',)
	ordering = ('expire_time',)

	# Detail Page Settings
	fieldsets = (
		('Base User', {'fields': ('edit_user',)}),
		('Code', {'fields': ('code',)}),
		('Timestamp', {'fields': ('expire_time', 'is_expired',)}),
	)
	readonly_fields = ('edit_user', 'is_expired',)

	def edit_user(self, obj):
		change_url = reverse('admin:users_user_change', args=(obj.user.id,))
		return mark_safe('<a href="%s">%s</a>' % (change_url, obj.user.email))


@admin.register(UserLog)
class UserLogAdmin(admin.ModelAdmin):
	# List display Settings
	list_display = ('user', 'type', 'ip', 'datetime',)
	search_fields = ('user',)
	# list_filter = ('is_expired',)
	ordering = ('datetime',)

	# Detail Page Settings
	fieldsets = (
		('Base User', {'fields': ('edit_user',)}),
		('Info', {'fields': ('type', 'ip', 'device', 'datetime',)}),
	)
	readonly_fields = ('type', 'ip', 'device', 'datetime',)

	def edit_user(self, obj):
		change_url = reverse('admin:users_user_change', args=(obj.user.id,))
		return mark_safe('<a href="%s">%s</a>' % (change_url, obj.user.email))


admin.site.unregister(BuiltInGroup)
