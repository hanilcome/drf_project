from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from users.models import User
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
    
    # 회원가입시 비밀번호를 해싱(암호화) 하는 함수
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

class UserModifySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        
    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        new_password = make_password(validated_data['password'])
        instance.password = new_password
        instance.save()
        return instance
    
    
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        return token