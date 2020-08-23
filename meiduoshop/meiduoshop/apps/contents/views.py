from django.shortcuts import render
from django.views import View
from goods.models import GoodsChannelGroup, GoodsCategory,GoodsChannel
from collections import OrderedDict
from contents.models import ContentCategory
# Create your views here.

class IndexView(View):
    def get(self, request):
        """提供首页广告界面"""
        # 查询商品频道和分类
        #categories = OrderedDict()
        categories=OrderedDict()
        channels = GoodsChannel.objects.order_by('group_id', 'sequence')
        #遍历所有频道
        for channel in channels:
            #获取当前频道所在的组
            group_id = channel.group_id  # 当前组
            #构造基本的数据框架：11个组
            if group_id not in categories:
                categories[group_id] = {'channels': [], 'sub_cats': []}

            #查询当前频道对应的一级类别
            cat1 = channel.category  # 当前频道的类别

            # 追加当前频道
            categories[group_id]['channels'].append({
                'id': cat1.id,
                'name': cat1.name,
                'url': channel.url
            })
            # 构建当前类别的子类别
            for cat2 in cat1.subs.all():
                cat2.sub_cats = []
                for cat3 in cat2.subs.all():
                    cat2.sub_cats.append(cat3)
                categories[group_id]['sub_cats'].append(cat2)
        
        contents = OrderedDict()
        content_categories = ContentCategory.objects.all()
        for content_category in content_categories:
            contents[content_category.key] = content_category.content_set.filter(status=True).order_by('sequence')
            
        # 渲染模板的上下文
        context = {
            'categories': categories,
            'contents':contents
        }
        return render(request, 'index.html', context)
