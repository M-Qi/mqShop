import re
from datetime import datetime, timedelta
from rest_framework.validators import UniqueValidator

from users.models import VerifyCode
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()


class SmsSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=11)
    def create(self, validated_data):

        return VerifyCode.objects.create(**validated_data)

    def validate_mobile(self,mobile):
        '''
        手机号码验证
        :param mobile:手机号码
        :return:验证后的手机号码
        '''
        # 是否已经注册
        if User.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError("手机号码已经存在")

        # 判断是否合法
        if not re.match(settings.REGEX_MOBILE,mobile):
            raise serializers.ValidationError("手机号码非法")

        # 判断验证码发送频率
        # 60s发送一次
        one_mintes_ago = datetime.now() - timedelta(hours=0,minutes=1,seconds=0)
        if VerifyCode.objects.filter(add_time__gt=one_mintes_ago,mobile=mobile).count():
            raise serializers.ValidationError("发送频率过快")

        return mobile

class UserRegSerializer(serializers.ModelSerializer):
    '''
    用户注册序列化器
    '''
    # 用户表里没有这个字段，这里需要添加一个字段
    code = serializers.CharField(required=True,write_only=True,max_length=4,min_length=4,
                                 error_messages={
                                     'blank':"请输入验证码",
                                     'required':"请输入验证码",
                                     'max_length':"验证码格式错误",
                                     'min_length':"验证码格式错误"
                                 },
                                 help_text='验证码')
    # 验证用户名是否存在
    username = serializers.CharField(label='用户名',help_text='用户名',required=True,allow_blank=False,
                                     validators=[UniqueValidator(queryset=User.objects.all(),message='用户名已经存在')])
    password = serializers.CharField(
        style={"input_type":"password"},label='密码',write_only=True,help_text='密码'
    )

    # 验证code
    def validate_code(self,code):
        # 用户注册，已post方式提交注册信息,post的数据都保存在initial_data里面
        # username就是用户注册的手机号,验证码按添加时间顺序倒叙，为了后面验证过期、错误等
        verify_records = VerifyCode.objects.filter(mobile=self.initial_data['username']).order_by('-add_time')

        if verify_records:
            # 最进的一个验证码
            last_record = verify_records[0]
            # 有效期为五分钟
            five_mintes_ago = datetime.now() - timedelta(hours=0,minutes=5,seconds=0)
            if five_mintes_ago > last_record.add_time:
                raise serializers.ValidationError('验证码过期')
            if last_record.code != code:
                raise serializers.ValidationError('验证码错误')
        else:
            raise serializers.ValidationError('验证码错误')

        return code
    def validate(self, attrs):
        '''
        所有字段
        :param attrs:是字段验证合法之后返回的dict
        :return:将修改后的数据返回
        '''
        attrs['mobile'] = attrs['username']
        del attrs['code']
        return attrs

    # 密码加密保存
    def create(self, validated_data):
        user = super(UserRegSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        fields = ['mobile','code','username','password']

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=30)
    class Meta:
        model = User
        fields = '__all__'
        # exclude = ['username']
        read_only_fields = ['id','username']





