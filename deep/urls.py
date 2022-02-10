"""deep URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from typing import Dict

from django.contrib import admin
from django.http import HttpRequest
from django.urls import path
from ninja import NinjaAPI

# 닌자를 임포트

# 닌자 객체화
api = NinjaAPI()

# 함수를 데코레이터로 감싸서 사용함
@api.get("/add")
def add(request: HttpRequest, a: int, b: int) -> Dict[str, int]:
    return {"result": a + b}


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),  # api에 등록된 모든 url들이 등록됨
]
