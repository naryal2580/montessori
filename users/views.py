from django.shortcuts import render
from django.http import HttpRequest
from django.views import View
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.views.generic import DetailView
from . import models
from django.contrib.auth.mixins import LoginRequiredMixin

class LoginView(View):

    def get(self, request):
        return render(request, "login.html")

    def post(self, request: HttpRequest):
        email = request.POST.get("email")
        password = request.POST.get("password")

        if not email:
            messages.add_message(request,messages.ERROR, "No Email Provided.", extra_tags="alert-danger")
            return render(request, "login.html")
        elif not password:
            messages.add_message(request,messages.ERROR, "No Password Provided.", extra_tags="alert-danger")
            return render(request, "login.html")
        
        user = authenticate(request,email=email,password=password)

        if not user:
            messages.add_message(request,messages.ERROR, "Invalid Email or Password", extra_tags="alert-danger")
            return render(request, "login.html")

        if user:
            login(request,user)

        if user.is_student:
            return redirect("/")
        elif user.is_teacher:
            return redirect("/")

        return render(request, "login.html")


class ProfileView(LoginRequiredMixin, View):
    
    def get(self, request):
        return render(request, "profile.html")



def logout_view(request):
    logout(request)
    return redirect("/")


            


                


        
