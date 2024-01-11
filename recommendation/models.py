from django.db import models
# from djongo.db import models
from django.contrib.auth.models import User

# Create your models here.
class Notes(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    title=models.CharField(max_length=200)
    description=models.TextField()
    def __str__(self):
        return self.title
    class Meta:
        verbose_name= "notes"
        verbose_name_plural= "notes"

class Member(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    SID= models.CharField(max_length=200)
    def __str__(self):
        return str(self.SID)
    
class Rating(models.Model):
    stars = models.IntegerField(default=0)

    def delete_session(self, request):
        if SESSION_RATING_ID in request.session:
            del request.session[SESSION_RATING_ID]
# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     image = models.ImageField(default='default.jpg', upload_to='profile_pics')
#     confirmed = models.BooleanField("Confirmed", default=False)

#     SID = models.IntegerField("SID", max_length=30, blank=True)
    
#     def __str__(self):
#         return f'{self.user.username} Profile'
#     def save(self, *args, **kwargs):
#         super().save(*args, **kwargs) 


class Prerequisits(models.Model):
    CourseID= models.IntegerField(null=True, default="NULL")
    PrerequisitID= models.IntegerField(null=True, default="NULL")
    PrerequisitsGroup= models.IntegerField(null=True, default="NULL")
    TakeTogether= models.IntegerField(null=True, default="NULL")
    
class CoursesOffering(models.Model):
    Course= models.IntegerField(null=True, default="NULL")
    Course_Name=models.TextField(null=True, default="NULL")
    Credit= models.IntegerField(null=True, default="NULL")
    Semester= models.IntegerField(null=True, default="NULL")
    def __str__(self):
        return self.Course

class studentMajorMinor(models.Model):
    SID= models.BigIntegerField(primary_key=True,null=False, default="NULL")
    Special=models.IntegerField(null=True, default="NULL")
    Major= models.IntegerField(null=True, default="NULL")
    Minor= models.IntegerField(null=True, default="NULL")
    def __str__(self):
         return str(self.SID)
    
class Registrations(models.Model):
    SID= models.BigIntegerField(null=True, default="NULL")
    Semester=models.IntegerField(null=True, default="NULL")
    Course= models.IntegerField(null=True, default="NULL")
    GradeID= models.IntegerField(null=True, default="NULL")
    def __str__(self):
        return self.SID +" "+ self.Semester


class CoursesInSpeciality(models.Model):
    Course= models.IntegerField(null=True, default="NULL")
    Speciality=models.IntegerField(null=True, default="NULL")
    Major= models.IntegerField(null=True, default="NULL")
    IsCompulsory= models.IntegerField(null=True, default="NULL")
    def __str__(self):
        return self.Course
