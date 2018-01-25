from rest_framework import serializers

from .models import Wallet, Balance, Transaction
from ..companies.serializers import BalanceTokenDetailSerializer, TokenDetail


class WalletBalanceSerializer(serializers.ModelSerializer):
	token = BalanceTokenDetailSerializer()

	class Meta:
		model = Balance
		fields = ('wallet',
		          'token', 'balance', 'updated')


class FullWalletSerializer(serializers.ModelSerializer):
	balances = WalletBalanceSerializer(many=True)

	class Meta:
		model = Wallet
		fields = ('investor_user',
		          'eth_address',
		          'created', 'updated')
		read_only_fields = ('eth_address', 'created', 'updated')


class FullTransactionSerializer(serializers.ModelSerializer):
	class Meta:
		model = Transaction
		fields = ('user',
		          'type', 'datetime',
		          'from_address', 'from_address_type', 'from_address_note',
		          'to_address', 'to_address_type', 'to_address_note',
		          'amount', 'token_code',)
		read_only_fields = ('datetime',)

	# Add description label for transaction model
	def create(self, validated_data):
		from_address = validated_data['from_address']
		tokens = TokenDetail.objects.filter(contract_address=from_address)
		if tokens:
			validated_data['from_address_type'] = 'ICO_CONTRACT'
			validated_data['from_address_note'] = tokens[0].company.name
		elif validated_data.user.wallet.eth_address == from_address:
			validated_data['from_address_type'] = 'MY_WALLET'
			validated_data['from_address_note'] = 'My Wallet'
		else:
			validated_data['from_address_type'] = 'OTHER'
			validated_data['from_address_note'] = ''

		to_address = validated_data['to_address']
		tokens = TokenDetail.objects.filter(contract_address=to_address)
		if tokens:
			validated_data['to_address_type'] = 'ICO_CONTRACT'
			validated_data['to_address_note'] = tokens[0].company.name
		elif validated_data.user.wallet.eth_address == to_address:
			validated_data['to_address_type'] = 'MY_WALLET'
			validated_data['to_address_note'] = 'My Wallet'
		else:
			validated_data['to_address_type'] = 'OTHER'
			validated_data['to_address_note'] = ''

		transaction = Transaction.objects.create(**validated_data)
		return transaction
