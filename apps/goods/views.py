from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from .serializers import GoodsSerializer,GoodCategorySerializer,CategorySerializer
from goods.models import Goods,GoodCategory
from rest_framework import status,generics,mixins,viewsets

# APIView完成商品列表页
# class GoodsListView(APIView):
#     '''
#     商品列表
#     '''
#     def get(self,request):
#         goods = Goods.objects.all()
#         goods_serialzer = GoodsSerializer(instance=goods,many=True)
#         return Response(data=goods_serialzer.data,status=status.HTTP_200_OK)

# 自定义列表分页
from rest_framework.pagination import PageNumberPagination
class GoodsPagination(PageNumberPagination):
    # 默认每页显示的个数
    page_size = 12
    # 可以动态改变每页显示的个数 在查询字符串后面？page_size=1
    page_size_query_param = 'page_size'
    # 页码参数
    page_query_param = 'page'
    # 最多显示多少页
    max_page_size = 100


from django_filters.rest_framework import DjangoFilterBackend
from .filters import GoodsFilter
from rest_framework import filters
class GoodsListViewSet(mixins.ListModelMixin,mixins.RetrieveModelMixin,viewsets.GenericViewSet):
    '''
    商品列表页
    '''
    # 分页
    pagination_class = GoodsPagination
    # 必须指定排序
    queryset = Goods.objects.all().order_by('id')
    serializer_class = GoodsSerializer

    # 添加一个新的过滤器，都需要在这里进行注册
    filter_backends = (DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter)
    # 设置filter的类为我们自定义的类
    filter_class = GoodsFilter
    # 设置搜索 "="：表示精确搜索，也可以使用各种正则表达式
    search_fields = ("=name",'goods_brief')
    # 排序
    ordering_fields = ('sold_num','shop_price')

class CategoryViewSet(mixins.ListModelMixin,mixins.RetrieveModelMixin,viewsets.GenericViewSet):
    '''
    商品分类列表数据
    '''

    queryset = GoodCategory.objects.filter(category_type=1)
    serializer_class = CategorySerializer


