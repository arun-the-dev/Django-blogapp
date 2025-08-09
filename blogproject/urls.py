"""
URL configuration for blogproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path,include

from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.views import LogoutView

from blogapp.views.auth import user_login,user_register,user_update,user_account,user_forget_password,verify_otp,reset_password,author_account
urlpatterns = [
    path('admin/', admin.site.urls),
    path("",include("blogapp.urls")),
    path("login/",user_login,name="login"),
    path("register/",user_register,name="register"),
    path("update/",user_update,name="update"),
    path("logout/",LogoutView.as_view(next_page = "login"),name="logout"),
    path("account/",user_account,name="user-account"),
    path("account/author/<int:author_id>/",author_account,name="author-account"),
    path("foregt-password/",user_forget_password,name="user-forget-password"),
    path("verify-otp",verify_otp,name="verify-otp"),
    path("reset-passord",reset_password,name="reset-password"),   
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)