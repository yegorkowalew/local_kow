from django.shortcuts import render

# Create your views here.

def register_user(request):
    return render(request, 'userprofile/register_user.html', {})
