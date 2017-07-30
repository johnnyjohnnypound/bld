from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate , login, logout
from django.contrib.auth.models import User
from pypinyin import pinyin,FIRST_LETTER

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

def register_view(request):
    nam='';fac='';gra='';pho='';passwd='';cod='';
    err = ''

    if request.POST:
        nam = request.POST['name']
        fac = request.POST['faculty']
        gra = request.POST['garde']
        pho = request.POST['phone']
        kd = request.POST.get('opt',None)
        passwd = request.POST['password']
        cod = request.POST['code']
        if not ( nam and fac and gra and pho and kd and passwd and cod):
            err = 'missInfo'

        if not err:
            if cod != User.objects.get(username='hiddenadmin').first_name:
                err = 'wrongCode'
            else:
                if User.objects.filter(first_name=nam):
                    err = 'alr'
        if not err:
            ww = pinyin(nam,style=FIRST_LETTER)
            un = ''.join( [x[0] for x in ww])
            while User.objects.filter(username=un):
                un = un + '_1'
            newM = User.objects.create_user(un,"%s.%s@%s.com"%(kd,pho,gra),passwd)
            newM.first_name = nam
            newM.last_name = fac
            newM.save()
            login(request,newM)
            return HttpResponseRedirect('/')


    context =   {
                'nam':nam,
                'fac':fac,
                'gra':gra,
                'passwd':passwd,
                'pho':pho,
                'cod':cod,
                'e':err,
                }

    return render(request,'accounts/register.html',context) 

