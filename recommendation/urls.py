from django.urls import path
from .import views


urlpatterns = [
    path('home/', views.home, name='home'),
    path('notes/', views.notes, name='notes'),
    path('delete_note/<int:pk>', views.delete_note, name='delete-note'),
    path('notes_detail/<int:pk>', views.NotesDetailView.as_view(), name='notes-detail'),
    path('homework/', views.homework, name='homework'),
    path('update_homework/<int:pk>', views.update_homework, name='update-homework'),
    path('delete_homework/<int:pk>', views.delete_homework, name='delete-homework'),
    path('todo/', views.todo, name='todo'),
    path('update_todo/<int:pk>', views.update_todo, name='update-todo'),
    path('delete_todo/<int:pk>', views.delete_todo, name='delete-todo'),
    path('wiki/', views.wiki, name='wiki'),
    path('courses/', views.courses, name='courses'),
    path('About_us/', views.About_us, name='About_us'),
    path('Login/', views.Login, name='ert'),
    path('GPACalculator/', views.GPACalculator, name='GPACalculator'),
]
# <link rel="stylesheet" type="text/css" href="{% static 'blog/css/style.css' %}">
