from django.shortcuts import render, redirect
from django.views import View
from django import http
from django.db import DatabaseError
from users.models import User, Address
from django.urls import reverse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin
import json
#from celery_tasks.email.tasks import send_email_verify_url
# Create your views here.

class AddressCreateView(LoginRequiredMixin,View):
    def post(self, request):
        json_str = request.body.decode()
        json_dict = json.loads(json_str)
        receiver = json_dict.get('receiver')
        province_id = json_dict.get('province_id')
        city_id = json_dict.get('city_id')
        district_id = json_dict.get('district_id')
        place = json_dict.get('place')
        mobile = json_dict.get('mobile')
        tel = json_dict.get('tel')
        email = json_dict.get('email')

        address = Address.objects.create(
            user=request.user,
            tittle = receiver,
            receiver = receiver,
            mobiel=mobile,
            tel=tel,
            email=email
        )
        return http.JsonResponse({'code':0, 'errmsg':'ok'})

class AddressView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'user_center_site.html')
    def post(self, request):
        """查询收货地址"""
        # 核心逻辑：查询当前登录用户未被逻辑删除的地址
        address_model_list = request.user.addresses.filter(is_deleted=False)

        # 将地址模型列表转字典列表
        address_dict_list = []
        for address in address_model_list:
            address_dict = {
                "id": address.id,
                "title": address.title,
                "receiver": address.receiver,
                "province": address.province.name,
                "city": address.city.name,
                "district": address.district.name,
                "place": address.place,
                "mobile": address.mobile,
                "tel": address.tel,
                "email": address.email
            }
            address_dict_list.append(address_dict)

        # 查询当前登录用户默认地址的ID
        default_address_id = request.user.default_address_id

        return http.JsonResponse({
            "code":0,
            "errmsg":"ok",
            "default_address_id":default_address_id,
            "addresses":address_dict_list
        })


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
