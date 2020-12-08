import xadmin
from .models import Goods,GoodCategory,GoodsImage,Banner,HotSearchWords,GoodsCategoryBrand,IndexAd
# Register your models here.

# 商品信息管理
class GoodsAdmin(object):
    # 显示的列
    list_display = ('name','click_num','sold_num','fav_num','goods_num','market_price','shop_price','goods_brief','goods_desc','is_new','is_hot','add_time')
    # 可以搜索的字段
    search_fields = ['name',]
    # 列表字段可以编辑的
    list_editable = ['is_hot']
    # 过滤器
    list_filter = ['name','click_num','sold_num','fav_num','goods_num','market_price']
    # 富文本编辑器
    style_fields = {"goods_desc":"ueditor"}

    # 在添加商品的时候可以添加图片
    class GoodsImagesInline(object):
        model= GoodsImage
        exclude = ['add_time']
        extra = 1
        style = 'tab'
    inlines = [GoodsImagesInline]


# 商品分类管理
class GoodsCategoryAdmin(object):
    list_display = ["name", "category_type", "parent_category", "add_time"]
    list_filter = ["category_type", "parent_category", "name"]
    search_fields = ['name', ]

# 首页轮播管理
class BannerAdmin(object):
    list_display = ['goods','image','index']

# 热词管理
class HotSearchWordsAdmin(object):
    list_display = ['keywords','index','add_time']

# 某一大类下的宣传商标
class GoodsCategoryBrandAdmin(object):
    list_display = ['category','image','name','desc']

    def get_context(self):
        context = super(GoodsCategoryBrandAdmin, self).get_context()
        if 'form' in context:
            context['form'].fields['category'].queryset = GoodCategory.objects.filter(category_type=1)
        return context

# 商品广告
class IndexAdAdmin(object):
    list_display = ['category','goods']



xadmin.site.register(IndexAd,IndexAdAdmin)
xadmin.site.register(Goods,GoodsAdmin)
xadmin.site.register(GoodCategory,GoodsCategoryAdmin)
xadmin.site.register(Banner,BannerAdmin)
xadmin.site.register(HotSearchWords,HotSearchWordsAdmin)
xadmin.site.register(GoodsCategoryBrand,GoodsCategoryBrandAdmin)



