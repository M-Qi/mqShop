"""mqShop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import xadmin
from django.urls import path,include
from django.views.static import serve
from django.conf import settings
from rest_framework.documentation import include_docs_urls
from rest_framework_jwt.views import obtain_jwt_token
from user_operation.views import UserFavViewSet
from goods import views
from rest_framework.authtoken import views as v
from rest_framework.routers import DefaultRouter,SimpleRouter
from users.views import SmsCodeViewset, UserViewset,Ca
router = DefaultRouter()
router.register(r'goods',views.GoodsListViewSet)
router.register(r'categorys',views.CategoryViewSet,basename='categorys')
router.register(r'code',SmsCodeViewset,basename='code')
router.register(r'users',UserViewset,basename='users')
router.register('user_all', Ca,basename='all'),
router.register(r'userfavs',UserFavViewSet,basename='userfavs')

# ('user_all/<int:pk>/', Ca.as_view({"get": "retrieve"}), )


urlpatterns = [
       path('xadmin/', xadmin.site.urls),
       path('ueditor/',include('DjangoUeditor.urls')),
       # 配置访问 media路由
       path("media/<path:path>/",serve,{"document_root":settings.MEDIA_ROOT}),
       # 配置drf 文档，title自定义
       path("docs",include_docs_urls(title='生鲜API文档')),
       # 配置drf登录
       path("api-auth/",include('rest_framework.urls')),
       # path("goods_list/",views.GoodsListView.as_view(),name='goods_list'),
       # 商品列表页
       path('',include(router.urls)),
       # 配置drf 的token
       # path('api-token-auth/',v.obtain_auth_token)
       # jwt的token认证接口
       path('jwt-auth/',obtain_jwt_token),
       path("login/",obtain_jwt_token),

]

