# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http.response import JsonResponse
from django.shortcuts import render, get_object_or_404


# Create your views here.
from company.models import Company


def display_company(request, company_id):
    company = get_object_or_404(Company, pk=company_id)
    return render(request, 'company.html',
        {'company':company})