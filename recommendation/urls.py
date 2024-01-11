from django.urls import path
from .import views


urlpatterns = [
    path('home/', views.home, name='home'),
   # path('login/', views.login, name='login'),
    path('courses/', views.courses, name='courses'),
    path('About_us/', views.About_us, name='About_us'),
    path('GPACalculator/', views.GPACalculator, name='GPACalculator'),
     path('notes/', views.notes, name='notes'),
     path('delete_note/<int:pk>', views.delete_note, name='delete-note'),
    path('notes_detail/<int:pk>', views.get_note, name='notes-detail')
]
# <link rel="stylesheet" type="text/css" href="{% static 'blog/css/style.css' %}">
