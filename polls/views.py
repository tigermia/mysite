from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import Question,Choice
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.urls import reverse
import mysql.connector


class MiaQuestion:
    def __init__(self, id, val):
        self.id = id
        self.val = val

class Person:
    def __init__(self, fName, lName, age):
        self.fName = fName
        self.lName = lName
        self.age = age

class Boss(Person):
    def __init__(self, fname, lname, age, luxuriousStuff):
        Person.__init__(self, fname, lname, age)
        self.luxuriousStuff = luxuriousStuff

class SuperBoss(Boss):
    def __init__(self, fname, lname, age, luxuriousStuff, charactors):
        Boss.__init__(self, fname, lname, age, luxuriousStuff)
        self.charactors = charactors

class Company:
    def __init__(self, name, address, boss):
        self.name = name
        self.address = address
        self.boss = boss
        self.employees = []


    def hireEmployee(self, emp):
        self.employees.append(emp)


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # print(latest_question_list)
    #template = loader.get_template('polls/index.html')

    miaList = ['Mary is real estate python!','Pan is realestate croc']

    html = '<ul>'
    for x in miaList:
        html = html + '<li>' + x + '</li>'
    html = html +'</ul>'

    conn = mysql.connector.connect(
             user='root',
             password='dweieiwei',
             host='127.0.0.1',
             database='django')

    mycursor = conn.cursor()

    mycursor.execute("SELECT id, question_text FROM polls_question order by pub_date desc")

    mySqlresult = mycursor.fetchall()

    print(mySqlresult)
    myresult = []

    # html ="<table>"
    for x in mySqlresult:
        obj = MiaQuestion(x[0],x[1])
        myresult.append(obj)
    #     html = html + "<tr><td>"+x[0] +"</td><td>"+x[1]+"</td></tr>"
    # html = html+"</table>"
    for o in myresult :
        print(o, o.id, o.val)

    luxStuff = ['Herms', 'Gucci', 'BV', 'Porch']
    chars = ['Charming','Caring','Sensitive','Humor']
    company = Company('Tiger Castle Inc.', '211 Tigerwood Way', SuperBoss('Mary', 'Huge', 25, luxStuff,chars))
    company.hireEmployee(Person('Dick', 'Smith', 35))
    company.hireEmployee(Person('Rich', 'Hugo', 25))
    company.hireEmployee(Person('Raja', 'Dalal', 33))
    company.hireEmployee(Person('Shin', 'Shin', 44))
    company.employees.sort(key=lambda x: x.age, reverse=True)

    context = {
        'latest_question_list': latest_question_list,
        'html': html,
        'mia':['Mary is real estate python!','Pan is realestate croc'],
        'sqlResult':myresult,
        'company': company

    }

    for emp in company.employees:
        print(emp.fName, emp.lName, emp.age)

    # return HttpResponse(template.render(context, request))
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
    # try:
    #     question = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
    #     raise Http404("Question does not exist")
    question = get_object_or_404(Question, pk=question_id)
    print(question.choice_set.all())

    return render(request, 'polls/detail.html', {'question': question})
    # return HttpResponse("You're looking at question %s." % question_id)

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))