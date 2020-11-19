from django.shortcuts import render
from .models import User
from rest_framework import viewsets, filters
from .serializer import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all() # 全てのデータを取得
    serializer_class = UserSerializer
