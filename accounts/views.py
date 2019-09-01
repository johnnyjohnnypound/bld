from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.models import User
from .models import Debater
from pypinyin import pinyin, FIRST_LETTER

# Create your views here.

def login_view(request):
    go_url = request.GET.get('next', '')

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
                # p = User.objects.get(first_name=name)
                p = Debater.objects.all().get(username=name)
            except:
                error = 'notFind'
        
        if(not error):
            user = authenticate(username=name,password=passwd)
            if user is not None:
                login(request, user)
                if request.user.is_authenticated:
                    if go_url == '':
                        go_url = '/score/'
                    return HttpResponseRedirect(go_url) 
            else:
                error = 'wrongPasswd'       

    # return render(request,'accounts/login.html',{'n':name,'p':passwd,'e':error,'go':go_url})
    return render(request,'accounts/login.html',{'n':name,'p':passwd,'e':error,'go':go_url})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

def register_view(request):
    
    if not Debater.objects.exists():
        Debater.objects.create()

    nam='';fac='';gra='';pho='';passwd='';cod=''
    err = '';mail='';nick=''

    if request.POST:
        nam = request.POST['name']
        fac = request.POST['faculty']
        gra = request.POST['garde']
        pho = request.POST['phone']
        kd = request.POST.get('opt',None)
        passwd = request.POST['password']
        cod = request.POST['code']

        nick = request.POST['nickname']
        mail = request.POST['e_mail']
        # mail = "11@qq.com"

        if not ( nam and fac and gra and pho and kd and passwd and cod and nick and mail):
            err = 'missInfo'

        if not err:
            # if cod != User.objects.get(username='hiddenadmin').first_name:
            # to be continued
            if cod != "code":
                err = 'wrongCode'
            else:
                # if User.objects.filter(first_name=nam):
                # 
                if Debater.objects.all().filter(first_name=nam):
                    err = 'alr'
                if Debater.objects.all().filter(username=nick):
                    err = 'username_alr'
        if not err:
            # ww = pinyin(nam, style=FIRST_LETTER)
            # un = ''.join( [x[0] for x in ww])
            # while User.objects.filter(username=un):
            # while Debater.objects.filter(username=un):
            #    un = un + '_1'
            # newM = User.objects.create_user(un,"%s.%s@%s.com"%(kd,pho,gra),passwd)
            newM = Debater.objects.create_user(nick, mail, passwd)
            newM.first_name = nam
            # newM.last_name = fac
            newM.init(nick, fac, pho, gra, kd)
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
                'nick':nick,
                'mail':mail,
                }

    return render(request,'accounts/register.html',context) 

