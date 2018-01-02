from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group as BuiltInGroup

from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import User, InvestorUser, CompanyUser, AnalystUser, InvestorVerification, IDVerification, VerificationCode
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
		('User Extension', {'fields': ('edit_investor', 'edit_company_user', 'edit_analyst')}),
		('Permissions', {'fields': ('is_investor', 'is_company_user', 'is_analyst', 'is_active', 'is_staff',)}),
		('Security', {'fields': ('last_login', 'last_login_ip', 'TOTP_enabled',)}),
		('Timestamp', {'fields': ('created', 'updated',)}),
	)
	readonly_fields = ('created', 'updated',
	                   'last_login', 'last_login_ip', 'TOTP_enabled',
	                   'is_investor', 'is_company_user', 'is_analyst', 'is_active', 'is_staff',
	                   'edit_investor', 'edit_company_user', 'edit_analyst',)

	def edit_investor(self, obj):
		if obj.is_investor:
			change_url = reverse('admin:users_investoruser_change', args=(obj.investor.id,))
			return mark_safe('<a href="%s">%s</a>' % (change_url, obj.investor.full_name))
		else:
			return '-'

	def edit_company_user(self, obj):
		if obj.is_company:
			change_url = reverse('admin:users_companyuser_change', args=(obj.company_user.id,))
			return mark_safe('<a href="%s">%s</a>' % (change_url, obj.company_user))
		else:
			return '-'

	def edit_analyst(self, obj):
		if obj.is_analyst:
			change_url = reverse('admin:users_user_change', args=(obj.analyst.id,))
			return mark_safe('<a href="%s">%s</a>' % (change_url, obj.analyst.full_name))
		else:
			return '-'

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
		('User Info', {'fields': ('avatar', 'first_name', 'last_name', 'nationality',)}),
		('Verification', {'fields': ('verification_level', 'id_verification', 'accredited_investor_verification',)}),
		('Timestamp', {'fields': ('created', 'updated',)}),
	)
	readonly_fields = ('created', 'updated', 'verification_level', 'edit_user')

	def edit_user(self, obj):
		change_url = reverse('admin:users_user_change', args=(obj.user.id,))
		return mark_safe('<a href="%s">%s</a>' % (change_url, obj.user.email))


@admin.register(AnalystUser)
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


@admin.register(CompanyUser)
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


@admin.register(IDVerification)
class IDVerificationAdmin(admin.ModelAdmin):
	# official_id_type = models.CharField(max_length=20, choices=ID_TYPE_CHOICES)
	# official_id = models.FileField(upload_to=official_id_dir, null=True, blank=True)
	# nationality = models.CharField(max_length=20, null=True, blank=True)
	pass


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
		('Base User', {'fields': ('user',)}),
		('Timestamp', {'fields': ('expire_time', 'is_expired',)}),
	)
	readonly_fields = ('user', 'is_expired',)


admin.site.unregister(BuiltInGroup)
