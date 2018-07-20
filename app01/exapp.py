#!/usr/bin/env python
#encoding:utf-8
from django.http.request import QueryDict
from django.urls import reverse
from django.utils.safestring import mark_safe

from app01 import models
from extraapp.server_model import v1


#userinfo表格显示

class ExtraAppUserInfo(v1.BaseExtraAdmin):
    def func(self,obj=None,is_header=False):
        if is_header:
            return "操作"
        else:
            #primary_key
            #方向生成url 要有namespace
            #当前app名称，当前model，namespace
            #方法1
            # print(type(obj)._meta.app_label,self.model_class._meta.app_label)
            # print(type(obj),self.model_class._meta.model_name)
            #方法2
            # from extraapp.server_model import v1
            # print(self.site.namespace)
            #name =app名称model名称change
            # name="{0}:{1}_{2}_change".format(self.site.namespace,
            #                                  self.model_class._meta.app_label,
            #                                 self.model_class._meta.model_name
            #                                  )
            #
            # url=reverse(name,args=(obj.pk,))
            # # print(url)
            param_dict = QueryDict(mutable=True)  # 设置get url为可修改，默认为不可修改
            if self.request.GET:
                param_dict['_changlistfilter'] = self.request.GET.urlencode()
            base_edit_url = reverse("{2}:{0}_{1}_change".format(self.app_label, self.model_name, self.site.namespace),
                                    args=(obj.pk,))
            base_del_url=reverse("{2}:{0}_{1}_delete".format(self.app_label, self.model_name, self.site.namespace),
                                    args=(obj.pk,))
            edit_url = "{0}?{1}".format(base_edit_url, param_dict.urlencode())

            detail_url = reverse('{0}:{1}_{2}_detail'.format(self.site.namespace, self.app_label, self.model_name),
                                 args=(obj.pk,))

            param_url = ""
            if len(self.request.GET):
                _change = QueryDict(mutable=True)
                _change['_change_filter'] = self.request.GET.urlencode()
                param_url = "?{0}".format(_change.urlencode())

            return mark_safe("<a href='{0}'>编辑</a> | <a href='{1}'>删除</a>  | <a href='{2}{3}'>查看详细</a> ".format(edit_url,base_del_url,detail_url,param_url))

    def checkbox(self,obj=None,is_header=False):
        if is_header:
            # return mark_safe("<input type='checkbox'>")
            return "选项"
        else:
            tag="<input name='pk' type='checkbox' value='{0}'>".format(obj.pk)
            return mark_safe(tag)
    #定制显示某列数据
    def comb(self,obj=None,is_header=False):
        if is_header:
            return "某列"
        else:
            return "%s-%s"%(obj.username,obj.email)

    def initial(self,request):
        """返回值为True，返回当前页，False返回首页"""
        pk_list=request.POST.getlist('pk')

        # print(pk_list)
        #self.model_class就可以操作数据库
        return True
    initial.text="初始化"

    def multi_del(self,request):
        pass

    multi_del.text = "批量删除"
    list_display=[checkbox,'id','username','email',comb,func]

    #action
    action_list = [initial,multi_del]
    from extraapp.utils.filter_code import FilterOption

    #自定义显示函数
    def email(self,option,request):
        from extraapp.utils.filter_code import FilterList
        queryset=models.UserInfo.objects.filter(id__gt=2)
        return FilterList(option,queryset,request)

    filter_list=[
        FilterOption('username',False,text_func_name="text_username",val_func_name="value_username"),
        FilterOption('email',False,text_func_name="text_email",val_func_name="value_email"),
        # FilterOption(email,False,text_func_name="text_email",val_func_name="value_email"),
        FilterOption('ug',True),
        FilterOption('m2m',False)
    ]
v1.site.register(models.UserInfo,ExtraAppUserInfo)

#role表格显示
class ExtraAppRole(v1.BaseExtraAdmin):

    def func(self,obj=None,is_header=False):
        if is_header:
            return "操作"
        else:
            #primary_key
            #方向生成url 要有namespace
            #当前app名称，当前model，namespace
            #方法1
            # print(type(obj)._meta.app_label,self.model_class._meta.app_label)
            # print(type(obj),self.model_class._meta.model_name)
            #方法2
            # from extraapp.server_model import v1
            # print(self.site.namespace)
            #name =app名称model名称change
            # name="{0}:{1}_{2}_change".format(self.site.namespace,
            #                                  self.model_class._meta.app_label,
            #                                 self.model_class._meta.model_name
            #                                  )
            #
            # url=reverse(name,args=(obj.pk,))
            # # print(url)
            param_dict = QueryDict(mutable=True)  # 设置get url为可修改，默认为不可修改
            if self.request.GET:
                param_dict['_changlistfilter'] = self.request.GET.urlencode()
            base_edit_url = reverse("{2}:{0}_{1}_change".format(self.app_label, self.model_name, self.site.namespace),
                                    args=(obj.pk,))
            base_del_url=reverse("{2}:{0}_{1}_delete".format(self.app_label, self.model_name, self.site.namespace),
                                    args=(obj.pk,))
            edit_url = "{0}?{1}".format(base_edit_url, param_dict.urlencode())

            detail_url = reverse('{0}:{1}_{2}_detail'.format(self.site.namespace, self.app_label, self.model_name),
                                 args=(obj.pk,))

            param_url = ""
            if len(self.request.GET):
                _change = QueryDict(mutable=True)
                _change['_change_filter'] = self.request.GET.urlencode()
                param_url = "?{0}".format(_change.urlencode())

            return mark_safe("<a href='{0}'>编辑</a> | <a href='{1}'>删除</a>  | <a href='{2}{3}'>查看详细</a> ".format(edit_url,base_del_url,detail_url,param_url))
    list_display = ['id', 'name',func]
v1.site.register(models.Role,ExtraAppRole)

# v1.site.register(models.UserInfo)
# v1.site.register(models.Role)
class ExtraUserGroup(v1.BaseExtraAdmin):
    def func(self, obj=None, is_header=False):
        if is_header:
            return "操作"
        else:
            param_dict = QueryDict(mutable=True)  # 设置get url为可修改，默认为不可修改
            if self.request.GET:
                param_dict['_changlistfilter'] = self.request.GET.urlencode()
            base_edit_url = reverse("{2}:{0}_{1}_change".format(self.app_label, self.model_name, self.site.namespace),
                                    args=(obj.pk,))
            base_del_url = reverse("{2}:{0}_{1}_delete".format(self.app_label, self.model_name, self.site.namespace),
                                   args=(obj.pk,))
            edit_url = "{0}?{1}".format(base_edit_url, param_dict.urlencode())

            detail_url = reverse('{0}:{1}_{2}_detail'.format(self.site.namespace, self.app_label, self.model_name),
                                 args=(obj.pk,))

            param_url = ""
            if len(self.request.GET):
                _change = QueryDict(mutable=True)
                _change['_change_filter'] = self.request.GET.urlencode()
                param_url = "?{0}".format(_change.urlencode())

            return mark_safe(
                "<a href='{0}'>编辑</a> | <a href='{1}'>删除</a>  | <a href='{2}{3}'>查看详细</a> ".format(edit_url,
                                                                                                   base_del_url,
                                                                                                   detail_url,
                                                                                                   param_url))

    list_display = ['id', 'title', func]
v1.site.register(models.UserGroup,ExtraUserGroup)

"""
以上是完整示例
1、数据列表页面，定制显示列
    1.1 v1.site.register(models.UserInfo)，默认只显示对象列表
    
    1.2 v1.site.register(models.UserInfo,ExtraAppUserInfo) 
    class ExtraAppUserInfo(BaseExtraAdmin):#按照list_display中指定的字段进行显示
        list_display=[] 
        PS:字段可以
            字符串(必须是数据库的字段名)，
            函数，传参is_header=True 表示是表头，否则就是内容
"""