from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group as BuiltInGroup

from .models import User
from .forms import UserCreationForm


@admin.register(User)
class UserAdmin(BaseUserAdmin):
	# Add Form Settings
	add_form = UserCreationForm
	add_fieldsets = (
		(None, {
			'classes': ('wide',),
			'fields' : ('email', 'password1', 'password2'),
		}),
	)

	# List display Settings
	list_display = ('id', 'email', 'phone', 'created', 'last_login_ip')
	search_fields = ('email', 'phone')
	list_filter = ('created',)
	ordering = ('created',)

	# Detail Page Settings
	fieldsets = (
		('Account Info', {'fields': ('email', 'phone_prefix', 'phone', 'password')}),
		('Permissions', {'fields': ('is_investor', 'is_company', 'is_analyst', 'is_active', 'is_staff')}),
		('Security', {'fields': ('last_login', 'last_login_ip', 'TOTP_enabled')}),
		('Important dates', {'fields': ('created',)}),
	)
	readonly_fields = ('created', 'investor', 'last_login', 'last_login_ip')


# def account_info(self, obj):
# 	change_url = urlresolvers.reverse('admin:accounts_accountinfo_change', args=(obj.info.id,))
# 	account_info_instance = AccountInfo.objects.get(id=obj.info.id)
# 	return mark_safe('<a href="%s">%s</a>' % (change_url, account_info_instance))


admin.site.unregister(BuiltInGroup)
