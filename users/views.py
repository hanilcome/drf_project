from users.models import User
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import permissions
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from users.serializers import UserSerializer, CustomTokenObtainPairSerializer, UserModifySerializer
from rest_framework_simplejwt.views import (
    TokenObtainPairView
)

class UserView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"가입완료"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message":f"${serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST)


class UserModifyView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def put(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        
        if request.user == user:
            print(request.user, user, request.data["email"], user_id)
            serializer = UserModifySerializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response("회원정보가 수정되었습니다.",status=status.HTTP_200_OK)
            else:
                return Response("이미 존재하는 아이디 입니다!", status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        
        if request.user == user:
            user.delete()
            return Response("회원탈퇴가 정상적으로 되었습니다.",status=status.HTTP_200_OK)
        else:
            return Response("권한이 없습니다!",status=status.HTTP_200_OK)
            
            
class CustomTokenObtainPairView(APIView):
    def post(self, request):
        try:
            email = request.data.get("email", "")
            password = request.data.get("password", "")
            
            user = authenticate(request, email=email, password=password)
            
            user_serializer = UserSerializer(user)
            token = CustomTokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            
            response = Response(
                {
                    "message" : "로그인 성공",
                    "id" : user_serializer.data["id"],
                    "email" : user_serializer.data["email"],
                    "token" : {
                        "refresh" : refresh_token,
                        "access" : access_token,
                    }
                }
            )
            login(request, user)
            return response
        except AttributeError:
            return Response("email 또는 password가 다릅니다.", status=status.HTTP_403_FORBIDDEN)
    
    
class mockView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        serializer = UserSerializer(request.data)
        return Response({"접송중인 아이디" : serializer.data["email"]})
    