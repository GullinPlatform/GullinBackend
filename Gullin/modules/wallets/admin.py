from django.contrib import admin

from .models import Wallet, Balance, Transaction


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
	# List display Settings
	list_display = ('id', 'user', 'created', 'updated',)
	search_fields = ('user',)
	ordering = ('created',)

	# Detail Page Settings
	fieldsets = (
		('Wallet Info', {'fields': ('user', 'wallet_address',)}),
		('Timestamp', {'fields': ('created', 'updated',)}),
	)
	readonly_fields = ('created', 'updated', 'user', 'wallet_address',)


# TODO: Add balance and transactions to wallet admin


@admin.register(Balance)
class BalanceAdmin(admin.ModelAdmin):
	# List display Settings
	list_display = ('id', 'wallet_id', 'token_code', 'balance',)
	search_fields = ('token_code',)
	list_filter = ('token_code',)
	ordering = ('updated',)

	# Detail Page Settings
	fieldsets = (
		('Wallet', {'fields': ('wallet',)}),
		('Balance Detail', {'fields': ('token_code', 'balance',)}),
	)
	readonly_fields = ('wallet', 'token_code', 'balance',)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
	# List display Settings
	list_display = ('id', 'type', 'send_unit', 'receive_unit', 'datetime',)
	list_filter = ('datetime',)
	ordering = ('datetime',)

	# Detail Page Settings
	fieldsets = (
		('Wallet', {'fields': ('wallet',)}),
		('Transaction Detail', {'fields': ('type', 'datetime', 'send_type', 'send_address', 'send_amount', 'send_unit', 'receive_type', 'receive_address', 'receive_amount', 'receive_unit', 'price',)}),)
	readonly_fields = ('wallet', 'type', 'datetime',)
