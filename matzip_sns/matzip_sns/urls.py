"""matzip_sns URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from matzip_rest_api.views import views, login, evaluate

urlpatterns = [
    path('admin/', admin.site.urls),
    path('eval/', views.EvaluateViewSet.as_view({'get':'list', 'post':'create'})),
    path('user/', views.UserinfoViewSet.as_view({'get':'list', 'post':'create'})),
    path('login/', login.LoginView.as_view()),
    path('kakao_api/', views.KakaoLoginView.as_view()),
    path('naver_api/', views.NaverLoginView.as_view()),
    path('google_api/', views.GoogleLoginView.as_view()),
    path('post/', evaluate.EvaluateView.as_view()),
]
