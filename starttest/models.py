from django.db import models
from accounts.models import Test, Student, QuestionAnswer

# Create your models here.
class Result(models.Model) :
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    score = models.FloatField(default=0.0)

class StudentResponse(models.Model) :
    res = models.ForeignKey(Result, on_delete=models.CASCADE)
    ques = models.TextField()
    ans = models.TextField()
    status = models.BooleanField(default=False)
