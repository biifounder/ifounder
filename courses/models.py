from django.db import models

class Project(models.Model):
    name = models.CharField(max_length=500, unique=True)
    description = models.CharField(max_length=500,blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    edited_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name 
    

from django.db import models
from django.contrib.auth.models import AbstractUser
from embed_video.fields import EmbedVideoField



class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    username = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    year = models.CharField(max_length=200, null=True)
    gov = models.CharField(max_length=200, null=True)
    prov = models.CharField(max_length=200, null=True)
    school = models.CharField(max_length=200, null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


#_______________________________________________________________________________
class Year(models.Model):   
    k = models.CharField(max_length=400, default='1')    
    name = models.CharField(max_length=400)

class YearEval(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    k = models.CharField(max_length=400, default='1') 
    percent = models.PositiveSmallIntegerField(default=0) 

   
#_______________________________________________________________________________
class Subject(models.Model):
    k = models.CharField(max_length=400, default='1')
    p = models.CharField(max_length=400, default='1')
    name = models.CharField(max_length=400)    
    users = models.ManyToManyField(User, related_name='subjects') 

class SubjectEval(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    k = models.CharField(max_length=400, default='1')
    p = models.CharField(max_length=400, default='1')  
    score = models.PositiveSmallIntegerField(default=0) 
    total = models.PositiveSmallIntegerField(default=0) 
    percent = models.PositiveSmallIntegerField(default=0) 

#_______________________________________________________________________________
class Unit(models.Model):
    k = models.CharField(max_length=400, default='1')
    p = models.CharField(max_length=400, default='1')
    s = models.CharField(max_length=400, default='1')
    name = models.CharField(max_length=400)   

class UnitEval(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    k = models.CharField(max_length=400, default='1')
    p = models.CharField(max_length=400, default='1')  
    score = models.PositiveSmallIntegerField(default=0) 
    total = models.PositiveSmallIntegerField(default=0) 
    percent = models.PositiveSmallIntegerField(default=0) 
    


#_______________________________________________________________________________
class Lesson(models.Model):
    k = models.CharField(max_length=400, default='1')
    p = models.CharField(max_length=400, default='1')
    s = models.CharField(max_length=400, default='1')
    name = models.CharField(max_length=400)    

class LessonEval(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    k = models.CharField(max_length=400, default='1')
    p = models.CharField(max_length=400, default='1')  
    score = models.PositiveSmallIntegerField(default=0) 
    total = models.PositiveSmallIntegerField(default=0) 
    percent = models.PositiveSmallIntegerField(default=0) 

#_______________________________________________________________________________
class Outcome(models.Model):
    k = models.CharField(max_length=400, default='1')
    p = models.CharField(max_length=400, default='1')
    s = models.CharField(max_length=400, default='1')
    name = models.CharField(max_length=400)
    content = models.TextField( )
    img = models.ImageField(default=False)
    video = EmbedVideoField(default=False)    

class OutcomeEval(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    k = models.CharField(max_length=400, default='1')
    p = models.CharField(max_length=400, default='1')  
    score = models.PositiveSmallIntegerField(default=0) 
    total = models.PositiveSmallIntegerField(default=0) 
    percent = models.PositiveSmallIntegerField(default=0) 


#_______________________________________________________________________________

class Question(models.Model):
    k = models.CharField(max_length=400, default='1')
    q = models.CharField(max_length=400, default='1')
    p = models.CharField(max_length=400, default='1')
    l = models.CharField(max_length=400, default='1')
    u = models.CharField(max_length=400, default='1')
    s = models.CharField(max_length=400, default='1')
    name = models.TextField(null=True)
    op1 = models.CharField(max_length=200,null=True)
    op2 = models.CharField(max_length=200,null=True)
    op3 = models.CharField(max_length=200,null=True)
    op4 = models.CharField(max_length=200,null=True)
    hint = models.TextField(null=True)   
    level = models.CharField(max_length=400,null=True) 
    img = models.ImageField(default=False)
    video = EmbedVideoField(default=False)
    
class QEval(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    k = models.CharField(max_length=400, default='1')    
    score = models.SmallIntegerField(default=0) 
    flag =  models.PositiveSmallIntegerField(default=0) 


class QDubl(models.Model):
    k = models.CharField(max_length=400, default='1')
    q = models.CharField(max_length=400, default='1')
    p = models.CharField(max_length=400, default='1')
    name = models.TextField(null=True)
    op1 = models.CharField(max_length=200,null=True)
    op2 = models.CharField(max_length=200,null=True)
    op3 = models.CharField(max_length=200,null=True)
    op4 = models.CharField(max_length=200,null=True)
    hint = models.TextField(null=True)   
    level = models.CharField(max_length=400,null=True) 
    img = models.ImageField(default=False)
    video = EmbedVideoField(default=False)