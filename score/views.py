#coding:utf-8
from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse
from .models import record
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from operator import itemgetter

def index(request):
    members = User.objects.all()
    line = int(User.objects.get(username='hiddenadmin').last_name)

    lis = []

    for man in members:
        rs = record.objects.filter(who=man.username)
        s = 0
        for r in rs:
            s += r.soc

        if (s>0) or (man.email[0]=='0'):
            #print man.first_name
            if man.email[0] !='0':
                col = 'black'
            else:
                if s<line:
                    col = 'red'
                else:
                    col = 'green'

            lis.append({
                    'un' : man.username,
                    'name':man.first_name,
                    'sum': s,
                    'col': col
                })
        lis.sort(key=itemgetter('sum'),reverse=True)
        
        if request.user.is_authenticated:
            nam = request.user.first_name 
            un  = request.user.username
        else:
            nam = ''
            un = ''

    return render(request,'score/rank.html',{'list':lis,'name':nam,'un':un})

@login_required
def add(request):
    
    nam = request.user.first_name 
    un  = request.user.username
    
    if request.POST:
        kind = request.POST['kind']
        title = request.POST['title']
        detail = request.POST['detail']
        date = request.POST['date']
         
        if not (kind and title and detail and date):
            return HttpResponse("信息不全，罚你重填")

        score = {
                'zs':10,
                'mb':5,
                'bys':8,
                'cw':5,
                'other':0
                }
        kk = {
                'zs':"正赛",
                'mb':"模辩",
                'bys':"表演赛",
                'cw':"场务",
                'other':"待填写"
            }

        rc = record(
                kind = kk[kind],
                name = title,
                detail = detail,
                who = un,
                when = date,
                soc = score[kind]
                )
        rc.save();
        return HttpResponseRedirect("/score/")

    return render(request,'score/add.html',{'name':nam,'un':un})
