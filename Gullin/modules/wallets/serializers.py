from rest_framework import serializers

from .models import Wallet, Balance, Transaction


class FullVerificationCodeSerializer(serializers.ModelSerializer):
	class Meta:
		model = Wallet
		fields = ('user',
		          'wallet_address',
		          'created', 'updated')
		read_only_fields = ('wallet_address',)


class FullBalanceSerializer(serializers.ModelSerializer):
	class Meta:
		model = Balance
		fields = ('wallet',
		          'token_code', 'balance', 'updated')


class FullTransactionSerializer(serializers.ModelSerializer):
	class Meta:
		model = Transaction
		fields = ('wallet',
		          'type', 'datetime',
		          'send_type', 'send_address', 'send_amount', 'send_unit',
		          'receive_type', 'receive_address', 'receive_amount', 'receive_unit',
		          'price')
