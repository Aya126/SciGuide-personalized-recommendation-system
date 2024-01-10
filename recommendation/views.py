from django.shortcuts import redirect, render
from . forms import *
from django.contrib import messages
from django.views import generic
import requests
import wikipedia
# Create your views here.


def home(request):
    return render(request, 'pages/home.html', {})

def notes(request):
    if request.method == "POST":
        form = NotesForm(request.POST)
        if form.is_valid():
            notes = Notes(user=request.user, title=request.POST['title'], description=request.POST['description'])
            notes.save()
        messages.success(request,f"Notes Added from {request.user.username} Successfuly")    
    else:
        form = NotesForm()
    notes = Notes.objects.filter(user=request.user)
    context = {'notes':notes,'form':form}
    return render(request, 'pages/notes.html', context)

def delete_note(request,pk=None):
    Notes.objects.get(id=pk).delete()
    return redirect("notes")

class NotesDetailView(generic.DetailView):
    models = Notes
    def get_queryset(self):
        """Return Notes """
        return Notes.objects.order_by('id')

def homework(request):
    if request.method == "POST":
        form = NotesForm(request.POST)
        if form.is_valid():
           try:
               finished = request.POST['is_finished']
               if finished == 'on':
                   finished = True
               else:
                   finished = False  
           except:
               finished = False
               homeworks = Homework(user=request.user,
                                    subject = request.POST['subject'],
                                     title=request.POST['title'], 
                                    description=request.POST['description'],
                                    due = request.POST['due'],
                                    is_finished = finished
                                    )
           homeworks.save()
        messages.success(request,f"Homeworks Added from {request.user.username} Successfuly")    
    else:
       form = HomeworkForm()
    homework = Homework.objects.filter(user=request.user)
    if len(homework) == 0:
        homework_done = True
    else:
        homework_done = False

    context = {'homeworks':homework,'homeworks_done':homework_done,'form':form}
    return render(request, 'pages/homework.html',context)

def update_homework(request,pk=None):
    homework = Homework.objects.get(id=pk)
    if homework.is_finished == True:
        homework.is_finished = False
    else:
        homework.is_finished = True
    homework.save()
    return redirect('homework')

def delete_homework(request,pk=None):
    Homework.objects.get(id=pk).delete()
    return redirect("homework")

def todo(request):
    if request.method == "POST":
        form = TodoForm(request.POST)
        if form.is_valid():
           try:
               finished = request.POST['is_finished']
               if finished == 'on':
                   finished = True
               else:
                   finished = False  
           except:
               finished = False
               todos = Todo(user=request.user,
                                     title=request.POST['title'], 
                                    is_finished = finished)
           todos.save()
           messages.success(request,f"Todos Added from {request.user.username} Successfuly")    
    else:
       form = TodoForm()
    todo = Todo.objects.filter(user=request.user)
    if len(todo) == 0:
        todos_done = True
    else:
        todos_done = False
    context = {'todos':todo,'form':form,'todos_done':todos_done}
    return render(request, 'pages/todo.html', context)

def update_todo(request,pk=None):
    todo = Todo.objects.get(id=pk)
    if todo.is_finished == True:
        todo.is_finished = False
    else:
        todo.is_finished = True
    todo.save()
    return redirect('todo')

def delete_todo(request,pk=None):
    Todo.objects.get(id=pk).delete()
    return redirect("todo")

def wiki(request):
    if request.method == 'POST':
        text = request.POST['text']
        form = DashboardForm(request.POST)
        search = wikipedia.page(text)
        context = {
            'form':form,
            'title':search.title,
            'link':search.url,
            'details':search.summary
        }
        return render(request,"pages/wiki.html",context)
    else:
        form = DashboardForm()
        context = {'form':form}
    return render(request, 'pages/wiki.html', context)

def profile(request):
    homeworks = Homework.objects.filter(is_finished=False,user=request.user)
    todos = Todo.objects.filter(is_finished=False,user=request.user)
    if len(homeworks) == 0:
        homework_done = True
    else:
        homework_done = False
    if len(todos) == 0:
        todos_done = True
    else:
        todos_done = False
    context = {
        'homeworks':homeworks,
        'todos':todos,
        'homework_done': homework_done,
        'todos_done': todos_done
    }
    return render(request, 'pages/profile.html', context)

def courses(request):
    return render(request, 'pages/courses.html', {})

def About_us(request):
    return render(request, 'pages/About_us.html', {})


def Login(request):
    return render(request, 'pages/Login.html', {})


def GPACalculator(request):
    return render(request, 'pages/GPACalculator.html')
