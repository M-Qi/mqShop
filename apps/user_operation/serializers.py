from rest_framework import serializers
from user_operation.models import UserFav
from rest_framework.validators import UniqueTogetherValidator
from django.contrib.auth import get_user_model
User = get_user_model()

class UserFavSerializer(serializers.ModelSerializer):
    # 获取当前登录的用户
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        # validate实现唯一联合，一个商品只能收藏一次
        validators = [
            UniqueTogetherValidator(
                queryset=UserFav.objects.all(),
                fields=("user",'goods'),
                # message的信息可以自定义
                message='已收藏'
            )
        ]
        model = UserFav
        # 收藏的时候需要返回商品ID，因为取消收藏的时候必须知道商品的id是多少
        fields = ('user','goods','id')


class UserDetailSerializer(serializers.ModelSerializer):
    '''
    用户详情
    '''
    username = serializers.CharField(max_length=20)
    class Meta:
        model = User
        fields = ['name','gender','birthday','email','mobile','username']

