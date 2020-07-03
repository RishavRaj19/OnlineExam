from django.db import models

# Create your models here.
class Student(models.Model) :
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    classs = models.CharField(max_length=100)
    section = models.CharField(max_length=100)
    roll_no = models.CharField(max_length=100)
    mobile_no = models.CharField(max_length=100)
    school_code = models.CharField(max_length=100)

class Teacher(models.Model) :
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    mobile_no = models.CharField(max_length=100)
    school_code = models.CharField(max_length=100)

class Test(models.Model) :
    subject = models.CharField(max_length=100)
    classs = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    desc = models.TextField()
    author = models.CharField(max_length=100)
    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField()
    school_code = models.CharField(max_length=100)

class QuestionAnswer(models.Model) :
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    label = models.TextField()
    op1 = models.TextField()
    op2 = models.TextField()
    op3 = models.TextField()
    op4 = models.TextField()
    ans = models.TextField()