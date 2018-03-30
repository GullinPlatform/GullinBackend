from rest_framework import serializers

from .models import Wallet, Balance, Transaction
from ..companies.serializers import BalanceTokenDetailSerializer, TokenDetail


class WalletBalanceSerializer(serializers.ModelSerializer):
	token = BalanceTokenDetailSerializer()

	class Meta:
		model = Balance
		fields = ('token', 'balance', 'updated')


class FullTransactionSerializer(serializers.ModelSerializer):
	class Meta:
		model = Transaction
		fields = ('wallet', 'type', 'datetime',
		          'from_address', 'from_address_type', 'from_address_note',
		          'to_address', 'to_address_type', 'to_address_note',
		          'value', 'value_unit', 'tx_fee', 'tx_hash')

	# Add description label for transaction model
	def create(self, validated_data):
		# If no mark on from address type
		if not validated_data.get('from_address_type'):
			token = TokenDetail.objects.filter(token_address=validated_data['from_address'])
			if token:
				validated_data['from_address_type'] = 'TOKEN_SALE'
				validated_data['from_address_note'] = token[0].company.name
			else:
				validated_data['from_address_type'] = 'OTHER'
				validated_data['from_address_note'] = ''

		# If no mark on to address type
		if not validated_data.get('to_address_type'):
			token = TokenDetail.objects.filter(crowd_sale_contract_address=validated_data['to_address'])

			if token:
				validated_data['to_address_type'] = 'TOKEN_SALE'
				validated_data['to_address_note'] = token[0].company.name
			else:
				validated_data['to_address_type'] = 'OTHER'
				validated_data['to_address_note'] = ''

		transaction = Transaction.objects.create(**validated_data)
		return transaction


class FullWalletSerializer(serializers.ModelSerializer):
	balances = WalletBalanceSerializer(many=True)
	transactions = FullTransactionSerializer(many=True)

	class Meta:
		model = Wallet
		fields = ('id', 'eth_address',
		          'balances', 'transactions',
		          'created')
		read_only_fields = ('id', 'eth_address', 'created', 'balances')
