from django.shortcuts import render
from django.views import View
from django import http
from django.db import DatabaseError
from users.models import User

# Create your views here.
class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if not all([username, password, password2]):
            return http.HttpResponseForbidden('not')

        try:
            User.objects.create_user(username=username, password=password)
        except DatabaseError:
            return render(request, 'register.html', {'register_errmsg':'failure'})
        return http.HttpResponse('sucess')