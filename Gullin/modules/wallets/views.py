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

	def balance(self, request):
		"""
		Retrieve/Record user wallet balance info
		"""
		if request.method == 'GET':
			# Get the cached balance info from database
			serializer = FullWalletSerializer(request.user.investor.wallet)
			return Response(serializer.data)
		elif request.method == 'POST':
			#
			if request.data.get('new_balance'):
				for token_code, balance in request.data.get('new_balance').items():
					wallet_balances = request.user.investor.wallet.balances.all()
					wallet_balances.get(token__token_code=token_code).balance = balance
			return Response(status=status.HTTP_200_OK)

	def transaction(self, request):
		"""
		Retrieve/Record user transactions
		"""
		if request.method == 'GET':
			serializer = FullTransactionSerializer(request.user.investor.transacions)
			return Response(serializer.data)
		elif request.method == 'POST':
			serializer = FullTransactionSerializer(data=request.data)
			serializer.is_valid(raise_exception=True)

			return Response(serializer.data, status=status.HTTP_201_CREATED)
