from django.shortcuts import render

def brands(request):
    return render(request, 'skytheme/brands.html')