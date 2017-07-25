from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate , login, logout
from django.contrib.auth.models import User

# Create your views here.

def login_view(request):
    try:
        go_url = request.GET['next']
    except:
        go_url = '/'

    name   = ''
    passwd = ''
    error  = ''
    
    if request.POST:
        name = request.POST['name']
        passwd = request.POST['passwd']
        
        if(not name or not passwd):
            error = 'missInfo'
        
        if(not error):
            try:
                p = User.objects.get(first_name=name)
            except:
                error = 'notFind'
        
        if(not error):
            user = authenticate(username=p.username,password=passwd)
            if user is not None:
                login(request,user)
            else:
                error = 'wrongPasswd'

    if request.user.is_authenticated:
        return HttpResponseRedirect(go_url)

    return render(request,'accounts/login.html',{'n':name,'p':passwd,'e':error,'go':go_url})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

