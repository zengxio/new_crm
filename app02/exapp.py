#!/usr/bin/env python
#encoding:utf-8
from extraapp.server_model import v1
from app02 import models
v1.site.register(models.XX)
v1.site.register(models.OO)