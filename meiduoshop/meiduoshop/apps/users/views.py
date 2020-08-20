from django.shortcuts import render, redirect
from django.views import View
from django import http
from django.db import DatabaseError
from users.models import User
from django.urls import reverse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin
import json
#from celery_tasks.email.tasks import send_email_verify_url
# Create your views here.
class AddressCreateView(View):
    def post(self, request):
        pass

class AddressView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'user_center_site.html')

class EmailView(View):
    def put(self, request):
        json_str = request.body.decode()
        json_dict = json.loads(json_str)
        email = json_dict.get('email')
        try:
            request.user.email = email
            request.user.save()
        except Exception as e:
            return http.JsonResponse({'code':400})
        #send_email_verify_url.delay(email,  'www.itcast.cn')
        return http.JsonResponse({'code':0,'errmsg':'ok'})

class UserInfoView(LoginRequiredMixin, View):
    def get(self, request):
        context = {
            'username':request.user.username,
            'mobile':request.user.mobile,
            'email':request.user.email,
            'email_active':request.user.email_active
        }
        return render(request, 'user_center_info.html', context)


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
