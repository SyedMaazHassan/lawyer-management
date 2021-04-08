from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.http import HttpResponse
from django.http import JsonResponse
import json

total_plans = lawyer_plan.objects.all()

# main page function

def index(request):
    context = {}
    if not request.user.is_authenticated:
        return redirect("registration:index")
    
    return render(request, 'dashboard/index.html', context)


# function for signup

def signup(request):
    if request.method == "POST":
        name = request.POST['name']
        l_name = request.POST['l_name']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        context = {
            "name":name,
            "l_name":l_name,
            "email":email,
            "pass1":pass1,
            "pass2":pass2,
        }
        if pass1==pass2:
            if User.objects.filter(username=email).exists():
                print("Email already taken")
                messages.info(request, "Entered email already in use!")
                context['border'] = "email" 
                return render(request, "signup.html", context)

            user = User.objects.create_user(username=email, first_name=name, password=pass1, last_name=l_name)
            user.save()
            
            return redirect("application:login")
        else:
            messages.info(request, "Your pasword doesn't match!")
            context['border'] = "password"
            return render(request, "signup.html", context)


    
    return render(request, "signup.html")


# function for login

def login(request):

    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        context = {
            'email': email,
            'password': password
        }
        user = auth.authenticate(username=email, password=password)
        if user is not None:
            auth.login(request, user)
            if user.is_superuser:
                return redirect("admin/")
            else:
                return redirect("application:index")
        else:
            messages.info(request, "Incorrect login details!")
            return render(request, "dashboard/login.html", context)
            # return redirect("login")
    else:
        return render(request, "dashboard/login.html")


# function for logout

def logout(request):
    auth.logout(request)
    return redirect("application:index")



# getting all lawyer requests
def lawyer_requests(request):
    if request.user.is_authenticated and request.user.is_superuser:
        context = {}
        context['all_requests'] = lawyer.objects.filter(is_approved = False, is_rejected = False)
        context['all_approved'] = lawyer.objects.filter(is_approved = True)
        context['all_rejected'] = lawyer.objects.filter(is_rejected = True)
        return render(request, 'dashboard/lawyer-requests.html', context)
    return redirect("application:index")