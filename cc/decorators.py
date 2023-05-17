from functools import wraps
from django.contrib.auth import authenticate
from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect,HttpResponse
from .models import Student,Hod

def is_student_decorator(view_func):
    def wrapper_func(request,*args,**kwargs):
        user = request.user
        if user.is_authenticated:
            try:
                student = Student.objects.get(user_id=user.id)
            except Student.DoesNotExist:
                student = None
            if student is None:
                return HttpResponse("<h1>You are not authorised to view this page</h1>")
            if student.is_student:
                return view_func(request,*args,**kwargs)
            else:
                return HttpResponse("<h1>You are not authorised to view this page</h1>")
        else:
            return HttpResponse("<h1>You are not logged in</h1>")
    return wrapper_func
    return decorator

def is_hod_decorator(view_func):
    def wrapper_func(request,*args,**kwargs):
        user = request.user
        if user.is_authenticated:
            try:
                hod = Hod.objects.get(user_id=user.id)
            except Hod.DoesNotExist:
                hod = None
            if hod is None:
                return HttpResponse("<h1>You are not authorised to view this page</h1>")
            if hod.is_hod:
                return view_func(request,*args,**kwargs)
            else:
                return HttpResponse("<h1>You are not authorised to view this page</h1>")
        else:
            return HttpResponse("<h1>You are not logged in</h1>")
    return wrapper_func
    return decorator


