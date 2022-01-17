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
# django
from django.contrib import admin
from django.urls import path
from matzip_rest_api.views import views, login, evaluate, user, comment
# swagger
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.conf import settings
from django.urls import re_path


# # swagger
schema_view = get_schema_view(
    openapi.Info(
        title =" Matzip_SNS",
        default_version = 'v1',
        description = "share my matzip info",
        terms_of_service = "",
        contact = openapi.Contact(email="jch0apple@gmail.com"),
        license = openapi.License(name=""),
    ),
    validators = ['flex'],
    public = True,
    permission_classes = (permissions.AllowAny,)
)

urlpatterns = [
    # django
    path('admin/', admin.site.urls),
    path('eval/', evaluate.EvaluateView.as_view()),
    path('comment/', comment.CommentView.as_view()),
    # path('user/', views.UserinfoViewSet.as_view({'get':'list', 'post':'create'})),
    path('user/', user.UserView.as_view()),
    path('login/', login.LoginView.as_view()),
]

# swagger
if settings.DEBUG:
    urlpatterns += [
        re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name="schema-json"),
        re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    ]
