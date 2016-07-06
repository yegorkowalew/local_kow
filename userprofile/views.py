from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from .forms import RegisterUserForm
from django.contrib.auth.models import User
from userprofile.models import UserProfile

from django.contrib.auth import authenticate, login

def register_user(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            # process the data in form.cleaned_data as required
            
            return HttpResponseRedirect('/thanks/')
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
    return HttpResponseRedirect('/thanks/')
    
def user_detail(request, pk):
    m_user = get_object_or_404(User, username=pk)
    pr_user = UserProfile.objects.get(user_id=m_user.id)
    
    user = authenticate(username='0041703721', password='kisses85')
    login(request, user)
    
    return render(request, 'userprofile/user_profile.html', {
                                                        'm_user': m_user,
                                                        'pr_user': pr_user,
                                                        })    
