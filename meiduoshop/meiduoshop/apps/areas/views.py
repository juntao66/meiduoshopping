from django.shortcuts import render
from django.views import View
from django import http
from areas.models import Area
# Create your views here.

class AreasView(View):
    def get(self, request):
        area_id = request.GET.get('area_id')
        if not area_id:
            province = Area.objects.filter(parent__isnull=True)
            p_list = []
            for p_model in province:
                p_dict = {
                    "id":p_model.id,
                    "name":p_model.name
                }
                p_list.append(p_dict)
            return http.JsonResponse({'code':0, 'errmsg':'ok','province':p_list})
