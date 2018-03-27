#coding:utf-8
from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse
from .models import Record,Semester
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from operator import itemgetter
from re import findall,IGNORECASE
import os

def index(request):
    members = User.objects.all()
    line = int(User.objects.get(username='hiddenadmin').last_name)

    cur_sem_id = Semester.objects.get(current=True).id
    sem_id = int(request.GET.get('sem',cur_sem_id)) 
    
    sems = []
    for sem in Semester.objects.all():
        sems.append({
            'id': sem.id,
            'name':sem.name,
            'curr':sem.id == sem_id
            })

    lis = []

    for man in members:
        if man.email[0]=='5' and sem_id==cur_sem_id:
            continue
        rs = Record.objects.filter(sem=sem_id);
        s = 0
        for r in rs:
            if(r.who == man.username) or (('#'+man.username+'#') in r.who):
                s += r.soc

        if (s>0) or (man.email[0]=='0' and sem_id==cur_sem_id):
            #print man.first_name
            if man.email[0] !='0':
                col = 'black'
            else:
                if s<line:
                    col = 'red'
                else:
                    col = 'green'
            
            name = man.first_name
            if not request.user.is_authenticated:
                name = name[0:1] + ' *' * (len(name)-1)

            lis.append({
                    'un' : man.username,
                    'name':name,
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

    return render(request,'score/rank.html',{
        'sems':sems,
        'list':lis,
        'name':nam,
        'un':un,
        'is_staff':request.user.is_staff,
        'is_login':request.user.is_authenticated
        })

@login_required
def add(request):
    
    nam = request.user.first_name 
    un  = request.user.username
    
    score = {
                'zs':10,
                'mb':5,
                'bys':8,
                'pw':2,
                'cw':5,
                'out':5,
                'other':0
                }
    kk = {
                'zs':"正赛",
                'mb':"模辩",
                'bys':"表演赛",
                'pw':"新生赛评委",
                'cw':"场务",
                'out':"外派",
                'other':"待填写"
            }
       
    k_list = ['zs','mb','bys','pw','cw','out','other']

    if request.POST:
        kind = request.POST['kind']
        title = request.POST['title']
        detail = request.POST['detail']
        date = request.POST['date']
        

        if kind not in kk or not (kind and title and detail and date):
            return HttpResponse("<h1>信息不全，返回重填</h1>")

        sco = score[kind]
        if kind == 'zs':
            if 'win' in request.POST:
                sco += 5
            if 'best' in request.POST:
                sco += 3

        rc = Record(
                kind = kk[kind],
                name = title,
                detail = detail,
                who = un,
                when = date,
                soc = sco,
                sem = Semester.objects.get(current=True).id
                )
        rc.save();
        return HttpResponseRedirect("/score/")
    
    old_name = set([r.name
            for r in Record.objects.all()
            if r.kind in '正赛表演赛模辩论' 
            ])
    
    old_detail = set([r.detail
            for r in Record.objects.filter(sem=Semester.objects.get(current=True).id)
            if r.kind in '正赛表演赛模辩论' 
            ])

    return render(request,'score/add.html',{
        'name':nam,
        'un':un,
        'k_list':k_list,
        'kk':kk,
        'ss':score,
        'old_name':old_name,
        'old_detail':old_detail
        })

@staff_member_required
def addGroup(request):
    nam = request.user.first_name 
    un  = request.user.username

    if request.POST:
        s = "#"
        for p in request.POST.getlist('values',[]):
            s = s + p + '#'
        rc = Record(
                kind = '#',
                name = request.POST['title'],
                detail = (u'记录人: ' + nam).encode('utf-8'),
                who = s,
                when = request.POST['date'],
                soc = int(request.POST['score']),
                sem = Semester.objects.get(current=True).id
                )
        rc.save();

        return  HttpResponseRedirect("/score/")
    
    members = User.objects.exclude(username='hiddenadmin').order_by('username');
    
    return render(request,'score/addGroup.html',{
        'members':members,
        'name':nam,
        'un':un
        });

@login_required
def ud(request,cun):
    try:
        cu = User.objects.get(username=cun)
    except:
        return HttpResponse(cun)

    ar1 = Record.objects.order_by("when")
    nam = request.user.first_name 
    
    ar = []
    for rr in ar1:
        if (rr.who==cun) or (('#'+cun+'#') in rr.who):
            ar.append(rr);


    pub_art = []
    path = '../member/'+cun+'/publicSpace/'
    if os.path.exists(path):
        for f in os.listdir(path):
            if (len(f)>5) and (f[-5:]=='.html'):
                FF = open(path+f,'r')
                text = FF.read()
                tt =  findall('<title>(.*?)</title>',text,flags=IGNORECASE)
                if tt:
                    title = tt[0]
                else:
                    title = f

                pub_art.append({
                        'f':f,
                        't':title
                    })
            


    context = {
            'ar':ar,
            'name':nam,
            'cun':cun,
            'cn':cu.first_name,
            'fac':cu.last_name,
            'gra':findall('@(\d+).com',cu.email)[0],
            'pa':pub_art
            }
    return render(request,'score/user.html',context)
 
@login_required
def us(request):
    nam = request.user.first_name 
    us = []
    for p in User.objects.all():
        ty = ''
        if p.email[0] == '0':
            ty = '考察期'
        elif p.email[0] == '1':
            ty = '正式队员'
        elif p.email[0] == '2':
            ty = '退役老兵'
        elif p.email[0] == '5':
            ty = '正式队员.'

        if ty:
            us.append({
                    'gra':findall('^.*?\..*?@(.*?)\.com$',p.email)[0],
                    'nam':p.first_name,
                    'fac':p.last_name,
                    'pho':findall('^.*?\.(.*?)@.*?\.com$',p.email)[0],
                    'ty':ty,
                    'un':p.username
                }
                )
    us.sort(key=itemgetter('gra'))
    return render(request,'score/users.html',{'us':us,'name':nam})

def getWho(s):
    if s[0]== '#':
        names = s[1:-1].split('#')
        ans = ''
        for name in names:
            ans = ans + ' ' + User.objects.get(username = name).first_name
        return ans[1:]
    else:
        return s

def getName(s):
    if s[0]== '#':
        names = s[1:-1].split('#')
        return "共计%d人"%(len(names))
    else:
        return User.objects.get(username = s).first_name

@login_required
def list(request):

    nam = request.user.first_name 
    if 'type' in request.GET:
        kf = request.GET['type']
    else:
        kf = ''
    lis = Record.objects.all() 

    lis = lis.order_by('when','kind','name','detail')

    l = [{
            'when':x.when,
            'who':getWho(x.who),
            'rn':getName(x.who), # User.objects.get(username = x.who).first_name,
            'kind':x.kind,
            'name':x.name,
            'detail':x.detail,
            'soc':x.soc
        } for x in lis if (kf in x.kind or x.kind in kf)]

    return render(request,'score/list.html',{'l':l,'name':nam})
