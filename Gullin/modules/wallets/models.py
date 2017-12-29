from django.db import models

from ..users.models import User


class Wallet(models.Model):
	# Link User
	user = models.OneToOneField('users.InvestorUser', related_name='wallet', on_delete=models.PROTECT)

	# Wallet Info
	wallet_address = models.CharField(max_length=100)

	# TimeStamp
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.user.full_name + ' wallet'


class Balance(models.Model):
	# Link to Wallet
	wallet = models.ForeignKey('Wallet', related_name='balances', on_delete=models.PROTECT)

	# Balance Info
	token_code = models.CharField(max_length=20)
	balance = models.FloatField()

	# TimeStamp
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return str(self.wallet) + ' balance'


class Transaction(models.Model):
	TRANSACTION_TYPE_CHOICES = (
		('TRANSACTION', 'TRANSACTION'),
		('DEPOSIT', 'DEPOSIT'),
	)

	DESTINATION_CHOICES = (
		('MY WALLET', 'MY WALLET'),
		('OUTSIDE WALLET', 'OUTSIDE WALLET'),
		('FINANCIAL SERVICE', 'FINANCIAL SERVICE'),
	)

	# Link to wallet
	wallet = models.ForeignKey('Wallet', on_delete=models.PROTECT)

	# Transaction Info
	type = models.CharField(choices=TRANSACTION_TYPE_CHOICES, max_length=20)
	datetime = models.DateTimeField(auto_now_add=True)

	send_type = models.CharField(choices=DESTINATION_CHOICES, max_length=20)
	send_address = models.CharField(max_length=200, null=True)
	send_amount = models.FloatField()
	send_unit = models.CharField(max_length=10)

	receive_type = models.CharField(choices=DESTINATION_CHOICES, max_length=20)
	receive_address = models.CharField(max_length=100, null=True)
	receive_amount = models.FloatField()
	receive_unit = models.CharField(max_length=10)

	price = models.FloatField()

	def __str__(self):
		return str(self.wallet) + ' transaction'
