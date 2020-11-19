from rest_framework import serializers # Django Rest Frameworkをインポート
from .models import User # models.py のcouponクラスをインポート

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User # 扱う対象のモデル名を設定する
        fields = '__all__'