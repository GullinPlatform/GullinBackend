from django.db import models

from ..users.models import User
from ..companies.models import TokenDetail


class Balance(models.Model):
	"""
	This model is only for cache, all user balance should be pulled on frontend, then store to database on backend,
	which means the balance on backend is NOT always up-to-date
	"""
	# Link to Wallet
	wallet = models.ForeignKey('Wallet', related_name='balances', on_delete=models.PROTECT)

	# Balance Info
	token = models.ForeignKey('companies.TokenDetail', related_name='balances', on_delete=models.PROTECT)
	balance = models.FloatField(default=0.0)

	# TimeStamp
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return str(self.wallet) + ' balance'


class Wallet(models.Model):
	"""
	The user wallet model, now only support ETH address and tokens issued on ETH blockchain
	"""
	# Link User
	investor_user = models.OneToOneField('users.InvestorUser', related_name='wallet', on_delete=models.PROTECT)

	# Wallet address
	eth_address = models.CharField(max_length=100, null=True, blank=True)

	# TimeStamp
	created = models.DateTimeField(auto_now_add=True)
	created_eth_block_num = models.IntegerField(default=5000000)

	def __str__(self):
		return self.investor_user.full_name + ' wallet'

	def init_balance(self):
		for token in TokenDetail.objects.all():
			Balance.objects.create(token_id=token.id, wallet=self)


class Transaction(models.Model):
	"""
	The purpose of this model is to record transactions happened to user's wallet
	"""
	TRANSACTION_TYPE_CHOICES = (
		('SEND', 'SEND'),
		('RECEIVE', 'RECEIVE'),
	)

	DESTINATION_CHOICES = (
		('MY_WALLET', 'MY_WALLET'),
		('ICO_CONTRACT', 'ICO_CONTRACT'),
		('OTHER', 'OTHER'),
	)

	# Link to wallet
	user = models.ForeignKey('users.InvestorUser', on_delete=models.PROTECT)

	# Transaction Info
	type = models.CharField(choices=TRANSACTION_TYPE_CHOICES, max_length=20)
	datetime = models.DateTimeField(auto_now_add=True)

	from_address = models.CharField(max_length=200, null=True)
	from_address_type = models.CharField(choices=DESTINATION_CHOICES, max_length=20)
	from_address_note = models.CharField(max_length=20)

	to_address = models.CharField(max_length=100, null=True)
	to_address_type = models.CharField(choices=DESTINATION_CHOICES, max_length=20)
	to_address_note = models.CharField(max_length=20)

	amount = models.FloatField()
	token_code = models.CharField(max_length=10)
	transaction_hash = models.CharField(max_length=100, null=True, blank=True)

	def __str__(self):
		return 'transaction of' + str(self.user)


class DepositRecord(models.Model):
	"""
	TODO:
	This model is for transaction like USD -> ETH.
	Since we are still uncertain about how to perform that,
	the design of this model is not finalized and is highly likely change in the future
	"""
	# Link to wallet
	wallet = models.ForeignKey('Wallet', on_delete=models.PROTECT)

	# Deposit Info
	deposit_amount = models.FloatField()
	currency_type = models.CharField(max_length=20)

	token_price = models.FloatField()
	token_code = models.CharField(max_length=20)
	token_receive_amount = models.FloatField()

	datetime = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return 'deposit to' + str(self.wallet)
