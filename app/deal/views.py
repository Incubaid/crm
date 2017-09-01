# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http.response import JsonResponse
from django.shortcuts import render

# Create your views here.

def hell(req):
    return JsonResponse({'a':1}, status=200)
