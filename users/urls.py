from django.urls import path
from users import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)

urlpatterns = [
    path('signup/', views.UserView.as_view(), name='user_view'),
    path('mock/', views.mockView.as_view(), name='mock_View'),
    path('login/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('modify/<int:user_id>/', views.UserModifyView.as_view(), name='Modify_View')
]