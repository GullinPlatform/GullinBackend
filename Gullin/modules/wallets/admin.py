from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import Wallet, Balance, Transaction


class BalanceInline(admin.TabularInline):
	model = Balance
	show_change_link = True
	fields = ('token_detail', 'balance')
	readonly_fields = ('token_detail', 'balance')
	extra = 0

	def token_detail(self, obj):
		change_url = reverse('admin:companies_tokendetail_change', args=(obj.token.id,))
		return mark_safe('<a href="%s">%s</a>' % (change_url, obj.token.token_code))


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
	# List display Settings
	list_display = ('id', 'investor_user', 'created',)
	search_fields = ('investor_user',)
	ordering = ('created',)

	# Detail Page Settings
	fieldsets = (
		('Wallet Info', {'fields': ('id', 'investor_user_detail', 'eth_address',)}),
		('Timestamp', {'fields': ('created', 'created_eth_block_num')}),
	)
	readonly_fields = ('id', 'created', 'created_eth_block_num', 'investor_user_detail', 'eth_address',)

	inlines = [BalanceInline, ]

	def investor_user_detail(self, obj):
		change_url = reverse('admin:users_investoruser_change', args=(obj.investor_user.id,))
		return mark_safe('<a href="%s">%s</a>' % (change_url, obj.investor_user.full_name))


@admin.register(Balance)
class BalanceAdmin(admin.ModelAdmin):
	# List display Settings
	list_display = ('id', 'wallet_id', 'token', 'balance',)
	search_fields = ('token',)
	list_filter = ('token',)
	ordering = ('updated',)

	# Detail Page Settings
	fieldsets = (
		('Wallet', {'fields': ('wallet_detail',)}),
		('Balance Detail', {'fields': ('token_detail', 'balance',)}),
	)
	readonly_fields = ('wallet_detail', 'token_detail', 'balance',)

	def token_detail(self, obj):
		change_url = reverse('admin:companies_tokendetail_change', args=(obj.token.id,))
		return mark_safe('<a href="%s">%s</a>' % (change_url, obj.token.token_code))

	def wallet_detail(self, obj):
		change_url = reverse('admin:wallets_wallet_change', args=(obj.wallet.id,))
		return mark_safe('<a href="%s">%s Wallet</a>' % (change_url, obj.wallet.investor_user.full_name))


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
	# List display Settings
	list_display = ('id', 'type', 'amount', 'token_code', 'from_address_type', 'to_address_type', 'datetime',)
	list_filter = ('datetime',)
	ordering = ('datetime',)

	# Detail Page Settings
	fieldsets = (
		('User', {'fields': ('edit_user',)}),
		('Transaction Detail',
		 {'fields': ('type', 'datetime',
		             'from_address', 'from_address_type', 'from_address_note',
		             'to_address', 'to_address_type', 'to_address_note',
		             'amount', 'token_code',)}),)
	readonly_fields = ('edit_user', 'from_address', 'to_address', 'datetime',)

	def edit_user(self, obj):
		change_url = reverse('admin:users_user_change', args=(obj.user.id,))
		return mark_safe('<a href="%s">%s</a>' % (change_url, obj.user.email))
