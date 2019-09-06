# -*- coding: utf-8 -*-

from django.shortcuts import render

def new_product_query_create(request):
    return render(request, 'oscar/customer/new_product_query/new_product_query_form.html', {})