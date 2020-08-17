from django.shortcuts import render, redirect
from django.views import View
from django import http
from django.db import DatabaseError
from users.models import User
from django.urls import reverse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
class UserInfoView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'user_center_info.html')


class LogoutView(View):
    def get(self, request):
        logout(request)
        response =  redirect(reverse('contents:index')) 
        response.delete_cookie('username')
        return response


class LoginView(View):
    def get(self, request):
        return render(request,  'login.html')
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        remembered = request.POST.get('remembered')
        print(username, password)

        if not all([username, password]):
            return http.HttpResponse('error1')

        user = authenticate(request=request, username=username, password=password)
        if user is None:
            return http.HttpResponse('error2')
        login(request, user)
        if remembered != 'on':
            request.session.set_expiry(0)
        else:
            request.session.set_expiry(None)
        #esponse = http.JsonResponse({'code':'0', 'r'})
        return redirect(reverse('contents:index'))

class UsernameCountView(View):
    def get(self, request, username):
        count = User.objects.filter(username=username).count()
        return http.JsonResponse({'code':'0', 'errmsg':'ok', 'count': count})

class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        mobile= request.POST.get('mobile')
        print(username,password)


        if not all([username, password]):
            return http.HttpResponseForbidden('not')

        try:
           user = User.objects.create_user(username=username, password=password, mobile=mobile)
        except DatabaseError:
            return http.HttpResponse('database error')
        
        login(request,  user)
        return redirect(reverse('contents:index'))
