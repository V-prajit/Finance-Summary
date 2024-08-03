from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Transaction, CustomRules, Tag, AdminRules
from .serializers import TransactionSerializer, TransactionWithTagsSerializer, AdminRulesSerializer, CustomRulesSerializer, TagSerializer

class TransactionListView(generics.ListAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)
    

class TransactionWithTagsView(generics.ListAPIView):
    serializer_class = TransactionWithTagsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user).prefetch_related('tags')
    
class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAdminUser]

class AdminRuleViewSet(viewsets.ModelViewSet):
    queryset = AdminRules.objects.all()
    serializer_class = AdminRulesSerializer
    permission_classes = [IsAdminUser]

class CustomRuleViewSet(viewsets.ModelViewSet):
    serializer_class = CustomRulesSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CustomRules.objects.filter(user=self.request.user)