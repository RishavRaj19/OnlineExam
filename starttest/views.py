from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
import time
from datetime import datetime, date
from accounts.models import QuestionAnswer, Student, Test
from .models import Result, StudentResponse

# Create your views here.
def checkValidity(request) :
    link = None
    if not request.user.is_authenticated :
        messages.info(request, 'You need to login first.')
        link = 'login'
        return link
    if request.user.is_staff :
        messages.info(request, 'Only student can give the test.')
        link = '/'
        return link

def result_page(request) :
    return render(request, 'result_page.html')

def result_page_student(request) :
    link = checkValidity(request)
    if link != None :
        return redirect(link)

    test_id = request.session['test_id']
    test = Test.objects.get(id=test_id)
    student = Student.objects.get(username=request.user.username)

    if Result.objects.filter(test_id=test_id, student_id=student.id).exists() :
        result = Result.objects.get(test_id=test_id, student_id=student.id)
        score = result.score
        return render(request, 'result_page_student.html', {'score':score, 'test':test, 'student':student})
    else :
        messages.info(request, "Data doesn't exists !")
        return render(request, 'error.html', {'link':'all_tests_student', 'link_name':'Available Test'})

def student_test_page(request) :
    link = checkValidity(request)
    if link != None :
        return redirect(link)

    if request.method == 'POST' :
        test_id = request.POST.get('test_id')
        student_id = Student.objects.get(username=request.user.username).id
        no_of_ques = request.POST['no_of_ques']

        if not Result.objects.filter(test_id=test_id, student_id=student_id).exists() :
            Result(test_id=test_id, student_id=student_id).save()
            res_id = Result.objects.get(test_id=test_id, student_id=student_id).id

            score = 0
            for i in range(1, int(no_of_ques)+1) :
                ques = request.POST['{}{}'.format('ques', i)]
                student_ans = request.POST.get('{}{}'.format('op', i))
                
                
                ques_id = request.POST['{}{}'.format('ques_id', i)]
                crct_ans = QuestionAnswer.objects.get(id=ques_id).ans

                status = False
                print(ques_id)
                print(crct_ans)
                print(student_ans)
                if crct_ans == student_ans :
                    score = score + 1
                    status = True
                
                print(score)
                StudentResponse(res_id=res_id, ques=ques, ans=student_ans, status=status).save()

            #update the score in result
            Result(id=res_id, test_id=test_id, student_id=student_id, score=score).save()
            
            messages.info(request, 'Test submitted successfully')
        else :
            messages.info(request, 'You have already given the test', {'link':'/', 'link_name':'Home'})

        return render(request, 'error.html', {'link':'/', 'link_name':'Home'})
    else :
        current_date = time.strftime('%Y.%m.%d %H:%M')

        test_id = request.session['test_id']
        test_start_date = request.session['starts_at']
        test_end_date = request.session['ends_at']
        
        print(test_end_date)

        if current_date > test_end_date :
            messages.error(request, 'The test has ended.')
            return render(request, 'error.html', {'link':'all_tests_student', 'link_name':'Available test'})
        elif current_date >= test_start_date :
            ques_ans_set = QuestionAnswer.objects.filter(test_id=test_id)
            return render(request, 'student_test_page.html', {'test_id':test_id, 'ques_ans_set':ques_ans_set})
        else :
            messages.info(request, 'The test will be starting at : ')
            return render(request, 'error.html', {'link':'all_tests_student', 'link_name':'Available test', 
                'countdown':test_start_date})    

    