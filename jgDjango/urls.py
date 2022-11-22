"""jgDjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
# [코드 추가] re_path 함수 추가로 불러오기
from django.urls import path, include
# [코드 작성] django.views.static에서 static 파일을 제공하기 위한 serve 함수 불러오기

# [코드 작성] django.conf에서 settings.py의 개체 가져오기


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('postings.urls')),
    path('games/', include('games.urls')),
    path('accounts/', include('accounts.urls')),
]

# [코드 작성] DEBUG가 False일 경우 static을 가져올 수 있도록 설정

