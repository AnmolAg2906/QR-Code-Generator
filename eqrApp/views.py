from django.shortcuts import redirect, render
import json
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse
from eqrApp import models, forms
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .models import Student


def context_data():
    context = {
        'page_name' : '',
        'page_title' : 'QR Generator',
        'system_name' : 'Student Data QR Code Generator',
        'topbar' : True,
        'footer' : True,
    }

    return context


# Create your views here.
def login_page(request):
    context = context_data()
    context['topbar'] = False
    context['footer'] = False
    context['page_name'] = 'login'
    context['page_title'] = 'Login'
    return render(request, 'login.html', context)

def login_user(request):
    logout(request)
    resp = {"status":'failed','msg':''}
    username = ''
    password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                resp['status']='success'
            else:
                resp['msg'] = "Incorrect username or password"
        else:
            resp['msg'] = "Incorrect username or password"
    return HttpResponse(json.dumps(resp),content_type='application/json')

@login_required
def home(request):
    context = context_data()
    context['page'] = 'home'
    context['page_title'] = 'Home'
    context['students'] = models.Student.objects.count()
    return render(request, 'home.html', context)

def logout_user(request):
    logout(request)
    return redirect('login-page')


@login_required
def student_list(request):
    context =context_data()
    context['page'] = 'student_list'
    context['page_title'] = 'Student List'
    context['students'] = models.Student.objects.all()

    return render(request, 'student_list.html', context)

@login_required 
def manage_student(request, pk=None):
    context =context_data()
    if pk is None:
        context['page'] = 'add_student'
        context['page_title'] = 'Add New student'
        context['student'] = {}
    else:
        context['page'] = 'edit_student'
        context['page_title'] = 'Update Student'
        context['student'] = models.Student.objects.get(id=pk)

    return render(request, 'manage_student.html', context)

@login_required
def save_student(request):
    resp = { 'status' : 'failed', 'msg' : '' }
    if not request.method == 'POST':
        resp['msg'] = "No data has been sent into the request."

    else:
        if request.POST['id'] == '':
            form = forms.SaveStudent(request.POST, request.FILES)
        else:
            student = models.Student.objects.get(id = request.POST['id'])
            form = forms.SaveStudent(request.POST, request.FILES, instance = student)
        if form.is_valid():
            form.save()
            if request.POST['id'] == '':
                messages.success(request, f"{request.POST['enrol_no']} has been added successfully.")
            else:
                messages.success(request, f"{request.POST['enrol_no']} has been updated successfully.")
            resp['status'] = 'success'
        else:
            for field in form:
                for error in field.errors:
                    if not resp['msg'] == '':
                        resp['msg'] += str("<br />")
                    resp['msg'] += str(f"[{field.label}] {error}")

    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def view_card(request, pk =None):
    if pk is None:
        return HttpResponse("Student ID is Invalid")
    else:
        context = context_data()
        context['student'] = models.Student.objects.get(id=pk)
        return render(request, 'view_id.html', context)

@login_required
def view_details(request, code = None):
    if code is None:
        return HttpResponse("Student code is Invalid")
    else:
        context = context_data()
        context['student'] = models.Student.objects.get(enrol_no=code)
        return render(request, 'view_details.html', context)

@login_required
def delete_student(request, pk=None):
    resp = { 'status' : 'failed', 'msg' : '' }
    if pk is None:
        resp['msg'] = "No data has been sent into the request."
    else:
        try:
            models.Student.objects.get(id=pk).delete()
            resp['status'] = 'success'
            messages.success(request, 'Student has been deleted successfully.')
        except:
            resp['msg'] = "Student has failed to delete."

    return HttpResponse(json.dumps(resp), content_type="application/json")