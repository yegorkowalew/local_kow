from django.shortcuts import render

from django.shortcuts import render
from django.http import HttpResponseRedirect

from .forms import RegisterUserForm

from django.contrib.auth.models import User
from userprofile.models import UserProfile

# Create your views here.

#def register_user(request):
#    return render(request, 'userprofile/register_user.html', {})

def register_user(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = RegisterUserForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = RegisterUserForm()

    return render(request, 'userprofile/register_user.html', {'form': form})

def pr(request):
    m_user = User.objects.get(username='0041703721')
    try:
        pr = UserProfile.objects.get(m_user.id)
    except:
        print('нету')
        user = UserProfile.objects.create(
                        user_id = m_user.id,
                        middle_name = 'Сергеевич'
        )
#    m_user.userprofile
#    print (pr)
    return HttpResponseRedirect('/thanks/')
