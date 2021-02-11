from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from django.http.response import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from polls.models import Question, Choice
from django.template import loader
from datetime import date, datetime

def index(request):
    qd = request.GET
    curPage = 1
    try:
        latest_question_list = Question.objects.order_by('-pub_date')[5*(int(qd["id"])-1):5*int(qd["id"])]
        curPage = int(qd["id"])
    except:
        latest_question_list = Question.objects.order_by('-pub_date')[0:5]
    pageCount = len(Question.objects.order_by('-pub_date'))
    pageCount = pageCount // 5 + (pageCount % 5 != 0)
    pages = []
    for i in range(1,pageCount+1):
        if (i == curPage):
            pages.append(True)
        else:
            pages.append(False)
    context = {
        'latest_question_list': latest_question_list,
        'pages': pages
    }
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question,pk=question_id)
    if(question.question_text == ""):
        question.delete()
        return redirect('index')
    return render(request,'polls/static.html',{'question':question})

def vote(request):
    qd = request.POST
    ch = Choice.objects.get(pk=int(qd['vote']))
    ch.votes += 1
    ch.save()
    context = {
        'question_id': int(qd['qid']),
        'question_text': Question.objects.get(pk=int(qd['qid'])).question_text,
        'choice_text': Choice.objects.get(pk=int(qd['vote'])).choice_text
    }
    return render(request,'polls/voted.html',context)
    #return HttpResponse("You voted in %s and chose %s" % (Question.objects.get(pk=int(qd['qid'])), Choice.objects.get(pk=int(qd['vote']))))

def edit(request,question_id):
    question = get_object_or_404(Question,pk=question_id)
    d = question.pub_date
    ch = question.choice_set.all()
    c = []
    for choice in ch:
        c.append(choice.choice_text)
    context = {
        'question_id': question_id,
        'date': d.strftime("%Y-%m-%d"),
        'question_text': question.question_text,
        'time': d.strftime("%H:%M"),
        'choices': c,
        'last_id': len(c)+1,
        'create_new': "false",
    }
    return render(request,'polls/edit.html',context)

def save(request):
    qd = request.POST
    quest = ""
    if(qd['createNew'] == "false"):
        id = int(qd['qid'])
        quest = get_object_or_404(Question,pk=id)
        quest.question_text = qd['qt']
        quest.pub_date = datetime.strptime(qd['date'] + ' ' + qd['time'], '%Y-%m-%d %H:%M')
        quest.choice_set.all().delete()
    else:
        quest = Question(question_text=qd['qt'],pub_date=datetime.strptime(qd['date'] + ' ' + qd['time'], '%Y-%m-%d %H:%M'))
        quest.save()
    m = qd['arrayChoice'].split('\0,')
    m[len(m)-1] = m[len(m)-1][:-1]
    for el in m:
        c = Choice(choice_text=el,votes=0,question=quest)
        c.save()
    return redirect('detail',quest.id)

def add(request):
    c = []
    context = {
        'question_id': 0,
        'date': datetime.now().strftime("%Y-%m-%d"),
        'question_text': "",
        'time': datetime.now().strftime("%H:%M"),
        'choices': c,
        'last_id': len(c)+1,
        'create_new': "true",
    }
    return render(request,'polls/edit.html',context)

def delete(request,question_id):
    question = get_object_or_404(Question,pk=question_id)
    question.delete()
    return redirect('index')