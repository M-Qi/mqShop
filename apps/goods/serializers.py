from rest_framework import serializers
from goods.models import Goods, GoodCategory, GoodsImage


# serializers 实现商品列表页

# class GoodsSerializer(serializers.Serializer):
#     name = serializers.CharField(required=True,max_length=100)
#     click_num = serializers.IntegerField(default=0)
#     goods_front_image = serializers.ImageField()



class GoodsImageSerializer(serializers.ModelSerializer):
    '''
    轮播图
    '''
    class Meta:
        model = GoodsImage
        fields = ('image',)


class GoodCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = GoodCategory
        fields = '__all__'



class GoodsSerializer(serializers.ModelSerializer):
    category = GoodCategorySerializer()
    images = GoodsImageSerializer()

    class Meta:
        model = Goods
        fields = '__all__'



class CategorySerializer3(serializers.ModelSerializer):
    class Meta:
        model = GoodCategory
        fields = "__all__"



class CategorySerializer2(serializers.ModelSerializer):
    '''
    二级分类
    '''
    #在parent_category字段中定义的related_name="sub_cat"
    sub_cat = CategorySerializer3(many=True)

    class Meta:
        model = GoodCategory
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    '''
    商品一级类别序列化
    '''
    sub_cat = CategorySerializer2(many=True)
    # sub_cat = serializers.StringRelatedField(many=True,read_only=True)
    class Meta:
        model = GoodCategory
        fields = '__all__'


