from django.shortcuts import render

from django.shortcuts import render
from django.http import HttpResponseRedirect

from .forms import RegisterUserForm


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


