from django.urls import path
from .views import TransactionListView

urlpatterns = [
    path('get-transactions/', TransactionListView.as_view(), name = 'transaction-list')
]