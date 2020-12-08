from django.shortcuts import render
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework.mixins import CreateModelMixin
from rest_framework import viewsets, status, mixins, authentication, permissions
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler

from user_operation.serializers import UserDetailSerializer
from users.models import VerifyCode
from .serializers import SmsSerializer,UserRegSerializer,UserSerializer
from random import choice
from utils.yunpian import YunPian
from rest_framework.response import Response
from django.conf import settings

# Create your views here.

# 获取User对象
User = get_user_model()

class CustomBackend(ModelBackend):
    '''
    自定义用户验证
    '''
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(
                Q(username=username) | Q(mobile=username)
            )
            if user.check_password(password):
                return user
        except Exception as e:
            return None

class SmsCodeViewset(CreateModelMixin,viewsets.GenericViewSet):
    '''
    获取手机验证码
    '''
    serializer_class = SmsSerializer

    def generate_code(self):
        '''
        生成四位数字验证码
        :return:
        '''
        seeds = '1234567890'
        random_str = []
        for i in range(4):
            random_str.append(choice(seeds))
        return ''.join(random_str)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        # 验证合法
        serializer.is_valid(raise_exception=True)
        # 从validated_data中取出手机号
        mobile = serializer.validated_data['mobile']

        yun_pian = YunPian(settings.APIKEY)
        # 生成验证码
        code = self.generate_code()

        sms_status = yun_pian.send_sms(code=code,mobile=mobile)
        print('sms_status==',sms_status)
        if sms_status['code'] != 0:
            return Response({
                'mobile':sms_status['msg'],
            },status=status.HTTP_400_BAD_REQUEST)
        else:
            # code_record = VerifyCode(code=code,mobile=mobile)
            serializer.save()
            return Response({
                'mobile':mobile
            },status=status.HTTP_201_CREATED)


class UserViewset(CreateModelMixin,mixins.UpdateModelMixin,mixins.RetrieveModelMixin,viewsets.GenericViewSet):
    '''
    用户
    '''
    serializer_class = UserRegSerializer
    queryset = User.objects.all()
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        re_dict = serializer.data
        payload = jwt_payload_handler(user)
        re_dict["token"] = jwt_encode_handler(payload)
        re_dict["name"] = user.name if user.name else user.username

        headers = self.get_success_headers(serializer.data)

        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)

    #这里需要动态权限配置
    #1.用户注册的时候不应该有权限限制
    #2.当想获取用户详情信息的时候，必须登录才行
    def get_permissions(self):
        if self.action == "retrieve":
            return [permissions.IsAuthenticated()]
        elif self.action == "create":
            return []

        return []

    #这里需要动态选择用哪个序列化方式
    #1.UserRegSerializer（用户注册），只返回username和mobile，会员中心页面需要显示更多字段，所以要创建一个UserDetailSerializer
    #2.问题又来了，如果注册的使用userdetailSerializer，又会导致验证失败，所以需要动态的使用serializer
    def get_serializer_class(self):
        if self.action == "retrieve":
            return UserDetailSerializer
        elif self.action == "create":
            return UserRegSerializer

        return UserDetailSerializer

    #虽然继承了Retrieve可以获取用户详情，但是并不知道用户的id，所有要重写get_object方法
    #重写get_object方法，就知道是哪个用户了
    def get_object(self):
        return self.request.user

    def perform_create(self, serializer):
        return serializer.save()


class Ca(viewsets.ViewSet):

    def list(self,request):
        print(self.action)
        users = User.objects.all()
        user = UserSerializer(instance=users,many=True,context={"request":request})
        print('user==',user)
        return Response(data=user.data,status=status.HTTP_200_OK)

    def retrieve(self,request,pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = UserSerializer(instance=user,context={"request":request})
        return Response(serializer.data,status=status.HTTP_200_OK)

    def create(self,request):
        user = UserSerializer(data=request.data)
        if user.is_valid():
            user.save()
        username = user.validated_data['username']
        print('username==',username)
        return Response(data=user.data,status=status.HTTP_200_OK)





