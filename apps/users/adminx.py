import xadmin
from xadmin import views
from .models import VerifyCode


# Register your models here.

class BaseSetting(object):
    # 添加主题功能
    enable_themes = True
    use_bootswatch = True

class GlobalSettings(object):
    # 全局配置
    site_title = '生鲜超市后台管理' #后台管理标题
    site_footer = 'https://www.baidu.com' # 页脚
    # 菜单收缩
    menu_style = 'accordion'

class VerifyCodeAdmin(object):
    list_display = ['code','mobile','add_time']


xadmin.site.register(views.CommAdminView,GlobalSettings)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(VerifyCode,VerifyCodeAdmin)

