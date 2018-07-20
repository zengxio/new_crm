#!/usr/bin/env python
#encoding:utf-8
from django.conf.urls import url,include
from django.contrib import admin
from app01 import views
urlpatterns = [
    url(r'^test/', views.test),
]