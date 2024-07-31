from django.urls import path
from .views import TransactionListView, TransactionWithTagsView

urlpatterns = [
    path('get-transactions/', TransactionListView.as_view(), name = 'transaction-list'),
    path('get-transaction-with-tags/', TransactionWithTagsView.as_view(), name='transaction-with-tags-list')

]