# -*- coding:utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from .forms import RegisterUserForm
from django.contrib.auth.models import User
from userprofile.models import UserProfile
from money.models import Post, Tarif

from django.contrib.auth import authenticate, login

def register_user(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = authenticate(username=request.POST['user_login'], password=request.POST['user_pass'])
            login(request, user)
            return HttpResponseRedirect('/user/'+request.user.username)
    else:
        form = RegisterUserForm()
    return render(request, 'userprofile/register_user.html', {'form': form})

    
def pr(request):
    m_user = get_object_or_404(User, username='0041703721')
    pr_user = UserProfile.objects.get(user_id=m_user.id)
    # new = Post(money=100, user=m_user)
    # new.save()
    money_last = Post.objects.filter(user=m_user).order_by('created_date').last()
    tarif_last = Tarif.objects.filter(user=m_user).last()
    print(tarif_last)
    if tarif_last:
        days_left = round(money_last.money/(tarif_last.money_for_mons/30))
    return render(request, 'userprofile/user_profile.html', {
                                                        'm_user': m_user,
                                                        'pr_user': pr_user,
                                                        'money_last':money_last,
                                                        'tarif_last':tarif_last,
                                                        'days_left':days_left,
                                                        })
    
def user_detail(request, pk):
    m_user = get_object_or_404(User, username=pk)
    pr_user = UserProfile.objects.get(user_id=m_user.id)
    # user = authenticate(username='0041703721', password='kisses85')
    # login(request, user)
    money_last = Post.objects.filter(user=m_user).order_by('created_date').last()
    return render(request, 'userprofile/user_profile.html', {
                                                        'm_user': m_user,
                                                        'pr_user': pr_user,
                                                        'money_last':money_last,
                                                        })
