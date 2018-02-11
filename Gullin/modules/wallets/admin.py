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


class TransactionInline(admin.TabularInline):
	model = Transaction
	show_change_link = True
	fields = ('type', 'datetime',
	          'from_address_type', 'to_address_type',
	          'value', 'value_unit', 'tx_hash', 'tx_fee',)
	readonly_fields = ('type', 'datetime',
	                   'from_address_type', 'to_address_type',
	                   'value', 'value_unit', 'tx_hash', 'tx_fee',)
	extra = 0


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

	inlines = [BalanceInline, TransactionInline]

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
	list_display = ('id', 'type', 'value', 'value_unit', 'from_address_type', 'to_address_type', 'datetime',)
	list_filter = ('datetime',)
	ordering = ('datetime',)

	# Detail Page Settings
	fieldsets = (
		('Wallet', {'fields': ('wallet_detail',)}),
		('Transaction Detail',
		 {'fields': ('type', 'datetime',
		             'from_address', 'from_address_type', 'from_address_note',
		             'to_address', 'to_address_type', 'to_address_note',
		             'value', 'value_unit', 'tx_hash', 'tx_fee',)}),)
	readonly_fields = ('wallet_detail', 'from_address', 'to_address', 'datetime', 'tx_hash',)

	def wallet_detail(self, obj):
		change_url = reverse('admin:wallets_wallet_change', args=(obj.wallet.id,))
		return mark_safe('<a href="%s">%s</a>' % (change_url, obj.wallet))
