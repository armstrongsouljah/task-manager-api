from django.shortcuts import render


# Create your views here.
def page(request):
    return render({'msg': 'test'})
