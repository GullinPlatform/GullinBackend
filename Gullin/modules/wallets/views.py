from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import FormParser, JSONParser

from .serializers import FullWalletSerializer, FullTransactionSerializer


class WalletViewSet(viewsets.ViewSet):
	"""
	The viewset for user authentication, includes sign_up, log_in, log_out, and verification
	"""
	parser_classes = (FormParser, JSONParser)
	permission_classes = (IsAuthenticated,)

	def wallet(self, request):
		"""
		Retrieve user wallet balance info
		"""
		# Get the cached balance info from database
		serializer = FullWalletSerializer(request.user.investor.wallet)
		return Response(serializer.data)

	def balance(self, request):
		"""
		Update user wallet balance info
		"""
		if request.data:
			for token_code, balance in request.data.items():
				wallet_balance = request.user.investor.wallet.balances.get(token__token_code=token_code)
				wallet_balance.balance = balance
				wallet_balance.save()
		return Response(status=status.HTTP_200_OK)

	def transaction(self, request):
		"""
		Record user transactions
		"""
		for transaction in request.data['transactions']:
			try:
				transaction['investor_user'] = request.user.investor.id
				serializer = FullTransactionSerializer(data=transaction)
				serializer.is_valid(raise_exception=True)
				serializer.save()
			except:
				pass
		return Response(status=status.HTTP_201_CREATED)
