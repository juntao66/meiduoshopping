from django.shortcuts import render
from django.views import View
from goods.models import GoodsCategory
from contents.utils import get_categories
from django import http
from goods.models import SKU
# Create your views here.
class DetailView(View):
    def get(self, request, sku_id):
        return render(request, 'detail.html')

class ListView(View):
    def get(self, request, category_id, page_num):
        try:
            category = GoodsCategory.objects.get(id=category_id)
        except:
            return http.HttpResponse('out')
        sort = request.GET.get('sort','default')
        if sort == 'price':
            sort_field = 'price'
        elif sort == 'hot':
            sort_field = '-sales'
        else:
            sort_field = 'create_time'
        categories = get_categories()
        
        skus = category.sku_set.filter(is_launched=True).order_by('sort_fiels')
        context = {
            'categories':categories,
            'sku':skus
        }
        return render(request, 'list.html', context)