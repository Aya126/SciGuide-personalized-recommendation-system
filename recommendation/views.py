from django.shortcuts import redirect, render, get_object_or_404
from . forms import *
from django.contrib import messages
from django.views import generic
import requests
import wikipedia
from django.contrib.auth.decorators import login_required
from .forms import RatingForm
from recommendation.testato import *
# Create your views here.

@login_required
def notes(request):
    if request.method == "POST":
        form = NotesForm(request.POST)
        if form.is_valid():
            notes = Notes(
                user=request.user, title=request.POST['title'], description=request.POST['description'])
            notes.save()
        messages.success(
            request, f"Notes Added from {request.user.username} Successfuly")
        return redirect("notes")
    else:
        form = NotesForm()
    notes = Notes.objects.filter(user=request.user)
    context = {'notes': notes, 'form': form}
    return render(request, 'pages/notes.html', context)

@login_required
def delete_note(request, pk=None):
    Notes.objects.get(id=pk).delete()
    return redirect("notes")
@login_required
def get_note(request, pk=None):
    nd= Notes.objects.get(id=pk)
    context = {'Notes': nd}
    return render(request, 'pages/notes_detail.html', context)

def rate_item(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    rating_id = request.session.get(SESSION_RATING_ID, None)

    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.item = item
            rating.save()
            rating.delete_session(request)
            request.session[SESSION_RATING_ID] = rating.id
            return redirect('item_detail', pk=item.pk)
    else:
        if rating_id:
            rating = get_object_or_404(Rating, pk=rating_id)
            form = RatingForm(instance=rating)
        else:
            form = RatingForm()

    return render(request, 'rate_item.html', {'form': form, 'item': item})

@login_required
def home(request):
    member = Member.objects.filter(user=request.user)
    context = {
        'members':member
    }
    return render(request, 'pages/home.html', context)

@login_required
def courses(request):
    # username = request.user.get_username()
    # print(username)
    # print('FROM VIEW', id)

    id = request.user.username
    courses_man, courses_not_man= predict(id)
    
    return render(request, 'pages/courses.html', {'courses_man':courses_man ,'courses_not_man':courses_not_man})

def About_us(request):
    return render(request, 'pages/About_us.html', {})


def register(request):
    form= UsersRegisterForm()
    if request.method == 'POST':
        form= UsersRegisterForm(request.POST)
        if form.is_valid():
             form.save()
             username=form.cleaned_data.get('username')
             messages.success(request,f"Account Creates for {username}")
             return redirect('login')
    else:
        form= UsersRegisterForm()

    context = {
        'form':form
    }
    return render(request, 'pages/register.html', {'form':form})

# def login(request):
#     form = UsersForm()
#     if request.method == 'Post':
#         form =  UsersForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('home')    
#         else:
#             form = UsersForm()
#             # context = {'form':form}
#     return render(request, 'pages/login.html', {'form':form})
#     # if request.method == 'Post':
#     #     userid= request.POST('ID')
#     #     user = authenticate(request, SID=userid)
#     #         if user is not None:
#     #             return render(request, 'pages/home.html', {})
#     #         else:
#     #             return redirect('pages/login.html')
#     #     except:
#     #          return redirect('/')
#     # else:
#     #     return render(request, 'pages/login.html')
#     # return render(request, 'pages/login.html')

def GPACalculator(request):
    return render(request, 'pages/GPACalculator.html')


