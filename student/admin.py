from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.conf import settings
from student.models import Student


class StudentAdmin(admin.ModelAdmin):
    '''
    '''
    # 配置展示列表
    list_display = ('student_num', 'name', 'class_name', 'teacher_name',
                    'gender', 'birthday')

    # 配置过滤查询字段
    list_filter = ('name', 'student_num')

    # 配置可以搜索字段
    search_fields = (['name', 'student_num'])

    # 设置只读字段
    readonly_fields = ('teacher',)

    # 定义列表显示顺序
    ordering = ('-created_at',)
    fieldsets = (
        (None, {
            'fields': ('student_num', 'name', 'gender', 'phone', 'birthday')
        }),
    )

    def save_model(self, request, obj, form, change):
        '''
        添加student表时，添加到 user 表
        由于需要和 teacher 表级联，所以自动获取当前登录的老师 id 作为 teacher_id

        :param request:
        :param obj:
        :param form:
        :param change:
        :return:
        '''
        if not change:
            user = User.objects.create(
                username=request.POST.get('student_num'),
                password=make_password(settings.STUDENT_INIT_PASSWORD)
            )
            obj.user_id = user.id
            obj.teacher_id = request.user.id
        super().save_model(request, obj, form, change)

    def delete_queryset(self, request, queryset):
        '''
        删除多条记录
        同时删除user表中数据
        批量删除，遍历 delete_queryset 中的 queryset

        :param request:
        :param queryset:
        :return:
        '''
        for obj in queryset:
            obj.user.delete()
            super().delete_model(request, obj)
        return

    def delete_model(self, request, obj):
        '''
        删除单挑数据
        同时删除user表中数据

        :param request:
        :param obj:
        :return:
        '''
        super().delete_model(request, obj)
        if obj.user:
            obj.user.delete()
        return


# 绑定 Teacher模型到 TeacherAdmin管理后台
admin.site.register(Student, StudentAdmin)
