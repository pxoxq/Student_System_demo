from django.contrib import admin
from teacher.models import Teacher
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


class TeacherAdmin(admin.ModelAdmin):
    # 配置显示列表
    list_display = ('name', 'email', 'class_name', 'gender', 'phone')
    # 配置过滤查询字段
    list_filter = ('class_name', 'name')
    # 配置可以搜索的字段
    search_fields = (['class_name', 'name'])
    # 定义每行显示数量
    list_per_page = 30
    # 定义显示排序
    ordering = ('-created_at',)
    # 显示字段
    fieldsets = (
        (None, {
            'fields': ('name', 'email', 'class_name', 'gender', 'phone')
        }),
    )

    def save_model(self, request, obj, form, change):
        user = User.objects.create(
            email=request.POST.get('email'),
            username=request.POST.get('email'),
            password=make_password(settings.TEACHER_INIT_PASSWORD),  # 密码加密？设置
            is_staff=1  # 允许作为管理员登陆后台
        )
        # 获取新增用户id，作为 tid 和 user_id
        obj.tid = obj.user_id = user.id
        super().save_model(request, obj, form, change)
        return

    def delete_queryset(self, request, queryset):
        '''
        删除多条数据
        同时删除user表中数据
        使用的是批量删除，所以需要遍历 delete_queryset 中的 queryset
        :param request:
        :param queryset:
        :return:
        '''
        for obj in queryset:
            obj.user.delete()
        # 这里可能出错
        super().delete_model(request, obj)
        return

    def delete_model(self, request, obj):
        '''
        :param request:
        :param obj:
        :return:
        删除单条数据，
        同时删除user表单
        '''
        super().delete_model(request, obj)
        if obj.user:
            obj.user.delete()
        return


# 设置后台页面头部显示内容和页面标题
admin.site.site_header = '智慧星学生管理系统'
admin.site.site_title = '智慧星学生管理系统'
# 绑定 Teacher 模型到 TeacherAdmin管理后台
admin.site.register(Teacher, TeacherAdmin)
