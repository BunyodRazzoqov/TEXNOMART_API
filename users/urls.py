from django.urls import path

from users.views import UserLoginApiView, UserLogoutApiView, UserRegisterAPIView

urlpatterns = [
    path('login/', UserLoginApiView.as_view()),
    path('logout/', UserLogoutApiView.as_view()),
    path('register/', UserRegisterAPIView.as_view()),
]
