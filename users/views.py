from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate

from .forms import FormWithCaptcha

def logout_view(request):

    logout(request)
    
    return HttpResponseRedirect(reverse('blog:index'))


def register(request):

    if request.method != 'POST':
        form = FormWithCaptcha()
    else:
        form = FormWithCaptcha(data=request.POST)
        print(request.POST)
        if form.is_valid():
            print('AAAAAAAA')
            new_user = form.save()
            authenticated_user = authenticate(username=new_user.username,
                                    password=request.POST['password1'])
            login(request, authenticated_user)                        
            return HttpResponseRedirect(reverse('blog:index'))

    context = {'form':form}

    return render(request, 'registration/register.html', context)