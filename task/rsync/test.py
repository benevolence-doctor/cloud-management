# -*- coding: utf8 -*-
import os
import sys

sys.path.append(r"C:\Users\gj\PycharmProjects\untitled3")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "untitled3.settings")
import django
django.setup()
from api.models import ProductName

print (ProductName.objects.get(productcode='ecs'))
print (ProductName.objects.filter(productcode='ecs').first())