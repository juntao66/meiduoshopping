from collections import OrderedDict
from  goods.models import GoodsChannel



def get_categories():
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
    return categories
