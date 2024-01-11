from django.contrib import admin
from . models import *
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

# class RecommendInLine(admin.StackedInline):
#     model= Member
#     can_delete= False
#     verbose_name_plural= 'Members'

# class customizedUserAdmin(UserAdmin):
#     inlines= (RecommendInLine, )
  

class CustomPrerequisits(admin.ModelAdmin):
    list_display=('CourseID', 'PrerequisitID', 'PrerequisitsGroup','TakeTogether')
    search_fields=['CourseID']

class Customstudentmajorminor(admin.ModelAdmin):
    list_display=('SID', 'Special','Major','Minor')
    list_filter= ['Major']
    search_fields=['Major']

class CustomCoursesoffering(admin.ModelAdmin):
    list_display=('Course', 'Course_Name','Credit','Semester')
    list_filter=['Semester']
    search_fields=['Semester']


class CustomCoursesinspeciality(admin.ModelAdmin):
    list_display=('Course', 'Speciality','Major','IsCompulsory')
    list_filter=['Speciality']
    search_fields=['Course']


class CustomRegistrations(admin.ModelAdmin):
    list_display=('SID', 'Semester','Course','GradeID')
    list_filter=['Semester']
    search_fields=['SID']

# admin.site.register(User)
# admin.site.register(User, customizedUserAdmin)

admin.site.register(Prerequisits,CustomPrerequisits)
admin.site.register(studentMajorMinor,Customstudentmajorminor)
admin.site.register(CoursesOffering,CustomCoursesoffering)
admin.site.register(Registrations,CustomRegistrations)
admin.site.register(CoursesInSpeciality,CustomCoursesinspeciality)
admin.site.register(Notes)

