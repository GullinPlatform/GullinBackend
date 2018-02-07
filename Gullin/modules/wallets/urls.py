from django.urls import path

from .views import WalletViewSet

wallet_retrieve = WalletViewSet.as_view({
	'get': 'wallet',
})

wallet_balance = WalletViewSet.as_view({
	'post': 'balance',
})

wallet_transaction = WalletViewSet.as_view({
	'get' : 'transaction',
	'post': 'transaction',
})

urlpatterns = [
	path('', wallet_retrieve, name='wallet_retrieve'),
	path('balance/', wallet_balance, name='wallet_balance'),
	path('transaction/', wallet_transaction, name='wallet_transaction'),
]
