from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AdminRuleViewSet, CustomRuleViewSet, TagViewSet, TransactionListView, TransactionWithTagsView


router = DefaultRouter()
router.register(r'admin-rules', AdminRuleViewSet)
router.register(r'custom-rules', CustomRuleViewSet, basename='customrule')
router.register(r'tags', TagViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('get-transactions/', TransactionListView.as_view(), name = 'transaction-list'),
    path('get-transaction-with-tags/', TransactionWithTagsView.as_view(), name='transaction-with-tags-list')
]