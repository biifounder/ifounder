from django.shortcuts import render,HttpResponse,redirect
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.auth.decorators import login_required
from .models import * 
from .forms import *
from json import dumps
from random import shuffle
from django.core.mail import send_mail

class HomeView(ListView):
    context_object_name = 'project_list'
    model = Project
    template_name = "courses/home.html"

class AboutView(TemplateView):
    template_name = "courses/about.html"

class ProjectCreateView(CreateView):
    model = Project
    fields = ['name', 'description']
    template_name = "courses/create.html"
    success_url ="/"

class ProjectEditView(UpdateView):
    model = Project
    fields = ['name','description']
    template_name = "courses/create.html"
    success_url ="/"

class ProjectDeleteView(DeleteView):
    model = Project
    template_name = "courses/delete.html"
    fields = ['name']
    success_url ="/"






def is_teacher(request): 
    if request.user.is_authenticated :  
        if request.user.email in  ['bahaaismailres@gmail.com','biifounder@gmail.com'] : 
            return request.user.username 
    return False

#======================================================================================================
def EmailSender(email_subject, message,receiver_emails):
        send_mail(
        email_subject,
        message,
        'bahaaismailres@gmail.com',
        receiver_emails,
        fail_silently=False,
        )


def AddUser(request, k):  
    user=request.user  
    subject = Subject.objects.get(k=k)
    subject.users.add(user)
    subject.save()
    if not YearEval.objects.filter(k=subject.p, user=user):
        YearEval.objects.create(k=subject.p, user=user)        
    s = subject.k
    SubjectEval.objects.create(k=k, user=user, p=subject.p)
    for unit in Unit.objects.filter(s=s): 
        UnitEval.objects.create(k=unit.k, user=user, p=unit.p)
    for lesson in Lesson.objects.filter(s=s): 
        LessonEval.objects.create(k=lesson.k, user=user, p=lesson.p)
    for outcome in Outcome.objects.filter(s=s): 
        OutcomeEval.objects.create(k=outcome.k, user=user, p=outcome.p)
    for question in Question.objects.filter(s=s): 
        QEval.objects.create(k=question.k, user=user)
    return redirect('open', subject.p)




def HomePage(request):
    if request.method == 'POST':   
        if "visitor" in request.POST:            
            y = request.POST.get('year') 
            yd = {'9':'التاسع','10':'العاشر'}
            y = yd[y]
            return redirect('open', Year.objects.get(name=y).k)     
            
        elif "register" in request.POST:          
            form = MyUserCreationForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.name = request.POST.get('name')
                user.email = request.POST.get('email')
                user.year = request.POST.get('year')
                user.gov = request.POST.get('gov')
                user.prov = request.POST.get('prov') 
                user.school = request.POST.get('school')                
                user.save()  
                login(request, user)
                yd = {'9':'التاسع','10':'العاشر'}
                yname = yd[user.year]    
                year = Year.objects.get(name=yname)  
                subjects = request.POST.get('selectedSubjects') 
                subjects = subjects.split(',')
                for s in subjects: 
                    subject = Subject.objects.get(name=s, p=year.k)
                    AddUser(request, subject.k)
                
                return redirect('home')  
            else: 
                return HttpResponse("يوجد خطأ في تسجيلك")   
        elif "login" in request.POST:            
            email=request.POST.get('email')
            pass1=request.POST.get('pass')
            user=authenticate(request,email=email,password=pass1)
            
            if user is not None:
                login(request,user) 
                return redirect('home')
            else:
                return HttpResponse ("كلمة السر خطأ")
        elif 'enquirey' in request.POST:
            email=request.POST.get('email')
            email_subject = 'from ' + email
            message = request.POST.get('message')
            EmailSender(email_subject, message, ['bahaaismailres@gmail.com'])
            return HttpResponse ("نشكركم على التواصل معنا وسوف يتم الرد على استفساركم في أقرب وقت ممكن إن شاء الله")   
    else:               
        if is_teacher(request) or not request.user.is_authenticated:             
            form = MyUserCreationForm()  
            context = {'teacher':is_teacher(request), 'years':Year.objects.all(), 'form':form}
            context['allusers'] = dumps([u.email for u in User.objects.all()])
            return render (request,'courses/home.html',context)
        else:             
            context = {'teacher':is_teacher(request)}   
            yd = {'9':'التاسع','10':'العاشر'}         
            y = User.objects.get(email=request.user).year
            y = yd[y]
            return redirect('open', Year.objects.get(name=y).k)
   

@login_required(login_url='login')
def Logout(request):
    logout(request)
    return redirect('home')


table = {
    'h':[ 'y' , '',   ''       ,  ''          ,  'الصفحة الرئيسية' ,  'الصفوف الدراسية' ],
    'y':[ 's' , 'h',   Year     ,  YearEval    ,  'صف'               ,  'المواد الدراسية' ],
    's':[ 'u' , 'y',   Subject  ,  SubjectEval ,  'مادة'             ,  'وحدات المادة'    ],
    'u':[ 'l' , 's',  Unit     ,  UnitEval    ,  'وحدة'             ,  'دروس الوحدة'     ],
    'l':[ 'o' , 'u',  Lesson   ,  LessonEval  ,  'درس'              ,  'مخرجات الدرس'    ],
    'o':[ 'q' , 'l',  Outcome  ,  OutcomeEval ,  'مخرج'             ,  ''                 ],
    'q':[ ''  , 'o',  Question ,  QEval          ,  'سؤال '            ,  ''                 ],
    'd':[ ''  , 'q',  QDubl ,  ''          ,  'سؤال '            ,  ''                 ],
}


def Object(request, k):
    context = {'teacher': is_teacher(request)} 
    if k == 'home': 
        context['years'] = Year.objects.all()
        return render (request,'courses/home.html',context)
    else: 
        user = request.user
        b, [c, g] = k[0], table[k[0]][:2]  
        object = table[b][2].objects.get(k=k)
        Child = table[c][2]            
        Eval, ChildEval = table[b][3], table[c][3]    
        context['b'] = b    
        context['gara'], context['ara'], context['cara'] = table[g][4], table[b][4], table[c][4]        
        context['p'] = 'home'
        context['reg'] = False
        if b != 'y':  
            context['p'] = object.p     
            context['grand'] = table[g][2].objects.get(k=object.p).name  
            if b == 's': 
                s = k
            else: 
                s = object.s 
            if Subject.objects.get(k=s).users.filter(email=str(user)):
                context['reg'] = True
        percent = 0 
        if request.user.is_authenticated and Eval.objects.filter(k=k, user=user): 
            percent = Eval.objects.get(k=k, user=user).percent
        context['percent'] = percent 
        
        if b == 's':
            context['test'] = []
            if object.users.filter(email=str(user)): 
                weaknesses = [] 
                for outc in Outcome.objects.filter(s=k): 
                    opercent = OutcomeEval.objects.get(k=outc.k).score
                    if int(opercent) < 70: 
                        weaknesses += [[opercent, outc.k, outc.name]] 
                weaknesses = sorted(weaknesses)
                context['weaknesses'] = [{'percent':w[0], 'wk':w[1], 'name':w[2]} for w in weaknesses]
            else:
                context['add'] = True
        if b == 'o': 
            context['object'] = object 
            context['contents'] = dumps( [ cont+'.' for cont in object.content.split('.')    ])
            questions = []
            for question in Question.objects.filter(p=k) : 
                questions += [question]+[q for q in QDubl.objects.filter(q=question.k)]
            context['questions'] = questions  
            return render (request,'courses/outcome.html', context)
        else:
            context['k'] = object.k
            context['name'] = object.name 
            context['contents'] = table[b][5]  
            children = []             
            creg = context['reg']
            for child in Child.objects.filter(p=k) : 
                cpercent = 0 
                if request.user.is_authenticated and ChildEval.objects.filter(k=child.k, user=user): 
                    cpercent = ChildEval.objects.get(k=child.k, user=user).percent                    
                if c == 's': 
                    if Subject.objects.get(k=child.k).users.filter(email=str(user)):
                        creg = True
                children += [{'ck':child.k, 'cname':child.name, 'cpercent':cpercent, 'creg':creg}]                       
            context['children'] = children
        return render (request,'courses/object.html', context)


fields = {
    'o': ['content', 'img', 'video'],
    'q': ['img', 'op1', 'op2', 'op3', 'op4', 'hint', 'video', 'level'], 
    'd': ['img', 'op1', 'op2', 'op3', 'op4'], 
}

def Create(request, p):
    if request.method == 'POST':  
        name = request.POST.get('name')   
        b, c = p[0], table[p[0]][0]        
        k = c
        [Obj, Eval] = table[c][2:4] 
        if c == 'q' or (b != 'h' and not Obj.objects.filter(p=p, name=name) or (b == 'h' and not Year.objects.filter(name=name))): 
            object, _ = Obj.objects.get_or_create(k=k, name=name)
            object.k += str(object.id)
            if c == 'q':
                object.q = object.k
            if b != 'h': 
                parent = table[b][2].objects.get(k=p)
                object.p = p
                if c == 'u': 
                    object.s = p 
                elif c in  ['l', 'o', 'q'] :
                    object.s = parent.s
                    if c in  ['o','q']:
                        childfields = fields[c]
                        for field in childfields: 
                            setattr(object, field, request.POST.get(field))
                        if c == 'q': 
                            lesson = Lesson.objects.get(k=parent.p)
                            object.l, object.u = parent.p, Unit.objects.get(k=lesson.p).k
            object.save()
            if c in ['q','o','l','u']: 
                subject = Subject.objects.get(k=object.s)
                Eval = table[c][3]
                for user in subject.users.all(): 
                    Eval.objects.create(k=k, user=user)
            return redirect('open', p)
        else: 
            return HttpResponse("هذا العنوان موجود بالفعل اضغط سهم العودة للتغيير") 
    else: 
        b = p[0]  
        c = table[b][0]
        context = {'teacher':is_teacher(request), 'child':c, 'cara':table[c][4]}     
    return render (request,'courses/create_update.html', context)



def Update(request, k):
    b = k[0]
    object = table[b][2].objects.get(k=k) 
    p = k  
    if b in ['q','d']: 
        p = object.p
    if request.method == 'POST':
        if request.POST.get('name') : 
            object.name = request.POST.get('name')
        if b in ['o','q']: 
            obfields = fields[b] 
            for field in obfields: 
                if request.POST.get(field) :  
                    setattr(object, field, request.POST.get(field))
        object.save()
        return redirect('open', p)
    context = {'teacher':is_teacher(request), 'child':b, 'object': object}
    return render(request, 'courses/create_update.html', context)


def Dublicate(request, k):
    if request.method == 'POST':
        dubl = QDubl.objects.get(k=request.session['nk'])        
        if request.POST.get('name') : 
            dubl.name = request.POST.get('name')
        obfields = fields['d'] 
        for field in obfields: 
            inp = request.POST.get(field) 
            if inp == '.' :
                setattr(dubl, field, '') 
            elif inp:
                setattr(dubl, field, inp)
        dubl.save()
        return redirect('open', dubl.p)
    else: 
        question = Question.objects.get(k=k) 
        QDubl.objects.create(k='d', q=k, p=question.p, name=question.name, img=question.img, hint=question.hint, video=question.video, 
                             op1=question.op1, op2=question.op2, op3=question.op3, op4=question.op4, level=question.level)
        dubl = QDubl.objects.get(k='d')
        dubl.k += str(dubl.id)
        dubl.save()   
        request.session['nk'] = dubl.k
        context = {'teacher':is_teacher(request), 'child':k[0], 'object': dubl}
    return render(request, 'courses/create_update.html', context)


def Delete(request, k):      
    if request.method == 'POST':  
        b = k[0]
        object = table[b][2].objects.get(k=k)
        p = object.p      
        object.delete()
        if b == 'q': 
            for dubl in QDubl.objects.get(k=object.k):
                dubl.delete()
        return redirect('open', p)
    return render(request, 'courses/delete.html')

#_________________________________________________________________________________________


def gatherQuestions(k): 
    if k.startswith('s'): 
        questions = [q for q in Question.objects.filter(s=k)]
    elif k.startswith('u'): 
        questions = [q for q in Question.objects.filter(u=k)]
    elif k.startswith('l'): 
        questions = [q for q in Question.objects.filter(l=k)]
    elif k.startswith('o'): 
        questions = [q for q in Question.objects.filter(p=k)]
    return questions
         

def MakeQuestions(user, k, nqs, reg): 
    questions = gatherQuestions(k) 
    shuffle(questions)
    if reg:        
        questionL = [] 
        for q in questions:
            ds = [q]+ [d for d in QDubl.objects.filter(q=q.k)]
            shuffle(ds)
            questionL += [ds[0]]
        
        if not nqs: 
            questions = [] 
            for f in [1,0]: 
                for l in ['1','2']: 
                    questions += [q for q in questionL if QEval.objects.filter(k=q.q, user=user, score=-1, flag=f) and q.level==l]
            for l in ['1','2']: 
                questions += [q for q in questionL if QEval.objects.filter(k=q.q, user=user, flag=1) and q.level==l and not q in questions]
            for s in [0,1]: 
                for l in ['1','2']:
                    questions += [q for q in questionL if QEval.objects.filter(k=q.q, user=user, score=s) and q.level==l and not q in questions]
        if nqs : 
            mcqL, shqs = [], []
            for s in (0,-1,1):
                qtemp = [q for q in questionL if QEval.objects.filter(k=q.q, user=user, score=s)]
                for q in qtemp : 
                    if q.op2: 
                        mcqL += [q]
                    else: 
                        shqs += [q]
            mcqs, exs = mcqL+[], []
            if len(mcqs) < nqs:        
                for s in shqs: 
                    new = [d for d in QDubl.objects.filter(q=s.q, user=user) if q.op2]  
                    if new:
                        shuffle(new)
                        mcqs += [new[0]]
                        exs += [s]
                        if len(mcqs) == nqs : 
                            break 
                for s in exs:
                    shqs.remove(s) 
            mcqs, shqs = mcqs[:nqs], shqs[:nqs]
            questions = mcqs+shqs
    else: 
        questions = questions[:3]

    JQuestions = []
    number = 1
    for q in questions:
        flag, score = 0,0 
        if reg: 
            Eval = QEval.objects.get(k=q.q, user=user) 
            flag, score = Eval.flag, Eval.score           
        d = {'k':q.q, 'question':q.name, 'img':'', 'hint':q.hint, 'video':'',
                'choice':'', 'delay':0, 'flagged':'', 
                'flag':flag, 'score':score} 
        if q.img: 
            d['img'] = q.img.url
        if q.video: 
            d['video'] = q.video
        number += 1
        if q.op2:
            options = [q.op1, q.op2]
            if q.op3: options+=[q.op3]
            if q.op4: options += [q.op4]
            shuffle(options)
            d['correct'] = q.op1 
            d['options'] = options                           
                            
        else: 
            d['answer'] = q.op1
            d['correct'] = '1' 
            d['options'] = ['1','0']
        JQuestions += [d]    
    return dumps(JQuestions)
 



def updateScores(request): 
    user = request.user
    submitted = request.POST.get('submitted')
    submitted = submitted.split(',')
    for j in range(0, len(submitted)-1, 3): 
        newEval = QEval.objects.get(k=submitted[j], user=user)         
        newEval.score = int(submitted[j+1])
        newEval.flag = int(submitted[j+2])
        newEval.save()
    return submitted[-1]

def objectAttrs(request, k):
    user = request.user
    b = k[0]
    object = table[b][2].objects.get(k=k)  
    objectEval = False
    if b != 'y': 
        objectEval = table[b][3].objects.get(k=k, user=user)   
    return b, user, object, objectEval



def Practice(request, k):    
    if request.POST: 
        if request.session['reg']:  
            updateScores(request)             
        return redirect('open', k)
    else: 
        user = request.user
        outcome = Outcome.objects.get(k=k)
        reg = False 
        if Subject.objects.get(k=outcome.s).users.filter(email=str(user)): 
            reg = True  
        questions = MakeQuestions(user, k, 0, reg)    
        context = {'object':outcome, 'k':k, 'questions':questions, 'purpose':'pract', 'reg':reg}    
        request.session['reg'] = reg 
    return render (request,'courses/practice.html', context)



def foundationLevel(user,k): 
    questions = gatherQuestions(k)
    corrects, foundations = 0, 0
    for q in questions : 
        if q.level == '1' : 
            foundations += 1 
        if QEval.objects.get(k=q.k, user=user).score == 1:
            corrects += 1
    if corrects <= foundations:
        return True
    return False  

dnqs = {'s':2, 'u':2, 'l':2, 'o':2}
def updatePercent(user,k): 
    def calcPercent(user, k) : 
        b = k[0]   
        Modeval = table[b][3] 
        Eval = Modeval.objects.get(k=k, user=user) 
        score, total, percent = Eval.score, Eval.total, 0   
        if total > 0 and score > 0:      
            percent = 100*round(score/total,2)
        if b in ['s','u','l']: 
            c = table[b][0]
            midEval = table[c][3]             
            midevals = [m for m in midEval.objects.filter(p=k, user=user)]
            midpercents = [meval.percent for meval in midevals]
            midpercent = sum(midpercents)/len(midpercents)
            percent = 0.4*midpercent+0.6*percent
        if int(total/dnqs[b])  == 1 : 
            percent = min(percent, 85)
        if foundationLevel(user,k):
            percent = min(percent, 50) 
        Eval.percent = int(round(percent))
        Eval.save()
        return Eval.p 
    while k[0] in ['o','l','u','s'] :         
        k = calcPercent(user, k) 
    if k[0] == 'y': 
        Eval = YearEval.objects.get(k=k, user=user) 
        subpercents = [s.percent for s in SubjectEval.objects.filter(p=k, user=user)]
        subEval = 0 
        if subpercents :
            subEval = sum(subpercents)/len(subpercents)
        Eval.percent = int(round(subEval)) 
        Eval.save()



def Assessment(request, k):          
    if request.POST:  
        _, user, object, objectEval = objectAttrs(request, k)        
        totalscore = updateScores(request)         
        objectEval.score += int(totalscore)  
        objectEval.save()
        updatePercent(user,k)
        return redirect('open', k) 
    else:        
        _, user, object, objectEval = objectAttrs(request, k)  
        nqs = 2
        objectEval.total += nqs 
        objectEval.save()        
        updatePercent(user,k)                         
        questions = MakeQuestions(user, k, nqs, True)  
        context = {'object':object, 'k':k, 'questions':questions, 'purpose':'test'}            
    return render (request,'courses/practice.html', context)

























#=======================================================================================================

# def deleteAll():
#     for Mod in [YearEval, SubjectEval, UnitEval, LessonEval, OutcomeEval, QEval] : 
#         Mod.objects.all().delete()
#     for Mod in [Year, Subject, Unit, Lesson, Outcome, Question, QDubl] : 
#         Mod.objects.all().delete()

# def zeroEvals(ModEval): 
#     for Eval in ModEval.objects.all():
#         Eval.score = 0
#         Eval.flag = 0
#         Eval.total = 0
#         Eval.percdnt = 0        
#         Eval.save()

# from pandas to Model
    # import pandas as pd    
    # School.objects.all().delete()
    # df = pd.read_csv('schools.csv')
    # for index, row in df.iterrows():
    #     print(row['school'], row['province'], row['governorate'])
    #     School.objects.create(school=row['school'], prov=row['province'], gov=row['governorate'])
        # print(row)
    # for s in School.objects.filter(prov='البريمي'): 
    #     print(s.school)

# def weeklyReport() 
    # for user in User.objects.all(): 
        # email_subject = 'التقرير الأسبوعي من المؤسس التفاعلي'
        # message = ''
        # for subject in user.subjects.all() : 
        #     percent = str(SubjectEval.objects.get(k=subject.k, user=request.user).percent)
        #     message += 'Yout score in ' + subject.name + ' is ' + percent + '%'
        # EmailSender(email_subject, message, [user.email])


# for subject in Subject.objects.all(): 
#     for user in subject.users.all(): 
#         user.subjects.add(subject)
#     print(subject.k,subject.users.all())

# for user in User.objects.all(): 
#     print(user.subjects.all())