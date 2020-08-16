from django.shortcuts import render, redirect
from django.views import View
from django import http
from django.db import DatabaseError
from users.models import User
from django.urls import reverse
from django.contrib.auth import login

# Create your views here.
class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        mobile= request.POST.get('mobile')


        if not all([username, password]):
            return http.HttpResponseForbidden('not')

        try:
           user = User.objects.create_user(username=username, password=password, mobile=mobile)
        except DatabaseError:
            return http.HttpResponse('database error')
        
        login(request,  user)
        return redirect(reverse('contents:index'))