from django.shortcuts import render
from rest_framework import generics, viewsets, permissions
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Transaction, CustomRules, Tag, AdminRules
from .serializers import TransactionSerializer, TransactionWithTagsSerializer, AdminRulesSerializer, CustomRulesSerializer, TagSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

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
    permission_classes = [permissions.IsAdminUser]

    def perform_create(self, serializer):
        rule = serializer.save()
        for user in User.objects.all():
            Transaction.reanalyze_all_for_user(user)

class CustomRuleViewSet(viewsets.ModelViewSet):
    serializer_class = CustomRulesSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CustomRules.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        rule = serializer.save(user=self.request.user)
        Transaction.reanalyze_all_for_user(self.request.user)