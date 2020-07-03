from django.shortcuts import redirect, render
from django.contrib.auth.models import User, auth
from .models import Student, Teacher, Test, QuestionAnswer
from django.contrib import messages
import time
from datetime import datetime, date
from django.http import request

# Create your views here.
def register(request) :
    if request.method == 'POST' :
        isTeacher = request.POST.get('isTeacher', False)
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        classs = request.POST['classs']
        section = request.POST['section']
        roll_no = request.POST['roll_no']
        mobile_no = request.POST['mobile_no']
        school_code = request.POST['school_code']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if isTeacher == 'on' :
            isTeacher = True

        if password1 == password2 :
            if not User.objects.filter(username=username).exists() :
                if not User.objects.filter(email=email).exists() :
                    if isTeacher :
                        User.objects.create_user(username=username, email=email, password=password1, is_staff=True).save()
                        Teacher(first_name=first_name, last_name=last_name, username=username, email=email,
                        mobile_no=mobile_no, school_code=school_code).save()
                        return redirect('login')
                    else :
                        User.objects.create_user(username=username, email=email, password=password1).save()
                        Student(first_name=first_name, last_name=last_name, username=username, email=email,
                        classs=classs, section=section, roll_no=roll_no, mobile_no=mobile_no, school_code=school_code).save()
                        return redirect('login')
                else :
                    messages.info(request, 'an account with this email exists')
            else :
                messages.info(request, 'username already exists')
        else :
            messages.info(request, 'password does not match')

        return redirect('register')
    else :
        return render(request, 'register.html')

def login(request) :
    if request.method == 'POST' :
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None :
            auth.login(request, user)
            print('logged in')
            if not user.is_staff :
                return redirect('/')
            else :
                return redirect('teacher')
        else :
            messages.info(request, 'creds does not match')
            return redirect('login')
    else :
        return render(request, 'login.html')

def logout(request) :
    auth.logout(request)
    print('logged out')
    return redirect('/')

def teacher(request) :
    if request.user.is_authenticated :
        if request.user.is_staff :
            return render(request, 'teacher.html')
        else :
            messages.info(request, 'You are not an admin')
            return redirect('/')
    else :
        messages.info(request, 'Login with admin id')
        return redirect('login')

def test(request) :
    link = checkValidity(request)
    if link != None :
        return redirect(link)

    if request.method == 'POST' :
        subject = request.POST['subject']
        classs = request.POST['classs']
        title = request.POST['title']
        desc = request.POST['desc']
        starts_at = request.POST['starts_at']
        ends_at = request.POST['ends_at']

        s_code = Teacher.objects.get(username=request.user.username).school_code
        testPossible = True
        if Test.objects.filter(school_code=s_code, classs=classs, starts_at=starts_at, ends_at=ends_at).exists() :
            testPossible = False
            
        tests = Test.objects.filter(school_code=s_code, classs=classs)
        for t in tests :
            s_at = t.starts_at
            e_at = t.ends_at
            

        if not testPossible :
            messages.info(request, 'There exists a test for this class at the specified date.')
            return redirect('test')
        else :
            Test(subject=subject, classs=classs, title=title, desc=desc, 
            starts_at=starts_at, ends_at=ends_at, author=request.user.email,
                school_code=s_code).save()

            request.session['test_id'] = Test.objects.get(school_code=s_code, classs=classs, starts_at=starts_at, ends_at=ends_at).id
            return redirect('ques_ans')
    else :
        return render(request, 'test.html')

def ques_ans(request) :
    link = checkValidity(request)
    if link != None :
        return redirect(link)

    if request.method == 'POST' :
        ques = request.POST['ques']
        op1 = request.POST['op1']
        op2 = request.POST['op2']
        op3 = request.POST['op3']
        op4 = request.POST['op4']

        crct_op = request.POST['op']
        ans = request.POST[crct_op]
        print(ans)

        if True :
            test_id = request.session['test_id']
            if not QuestionAnswer.objects.filter(test_id=test_id, label=ques).exists() :            
                

                QuestionAnswer(test_id=test_id, label=ques, op1=op1, op2=op2, op3=op3, op4=op4, ans=ans).save()
                
                if 'button1' in request.POST :
                    messages.info(request, 'add more question')
                    return redirect('ques_ans')
                if 'button2' in request.POST :
                    messages.info(request, 'test created successfully')
                    return redirect('teacher')
            else :
                messages.info(request, 'question exists in the test')
        else :
            messages.info(request, 'Answer is not set')

        return redirect('ques_ans')
    else :
        return render(request, 'ques_ans.html')

def all_tests(request) :
    if request.user.is_authenticated :
        if request.user.is_staff :
            s_code = Teacher.objects.get(username=request.user.username).school_code
            tests = Test.objects.filter(school_code=s_code)
            return render(request, 'all_tests.html', {'tests' : tests})
        else :
            messages.info(request, 'You are not an admin.')
            return redirect('/')
    else :
        messages.info(request, 'Login using admin id.')
        return redirect('login')

def all_tests_student(request) :
    link = checkValidity(request)
    if link != None :
        return redirect(link)

    if request.method == 'POST' :
        request.session['test_id'] = request.POST.get('test_id')
        request.session['starts_at'] = request.POST.get('starts_at')
        request.session['ends_at'] = request.POST.get('ends_at')

        if 'SubmitTest' in request.POST :
            return redirect('student_test_page')
        if 'GetResult' in request.POST :
            return redirect('result_page_student')
    else :
        user = Student.objects.get(username=request.user.username)
        school_code = user.school_code
        classs = user.classs

        tests = Test.objects.filter(school_code=school_code, classs=classs)
        return render(request, 'all_tests_student.html', {'tests' : tests})

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