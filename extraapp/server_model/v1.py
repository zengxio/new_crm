#!/usr/bin/env python
#encoding:utf-8

import copy

from django.http.request import QueryDict
from django.shortcuts import HttpResponse, render, redirect
from django.urls import reverse
from django.template.response import TemplateResponse, SimpleTemplateResponse

class BaseExtraAdmin(object):
    list_display="__all__"
    action_list=[]
    filter_list=[]
    add_or_edit_model_form=None
    change_form_template = []

    def __init__(self,model_class,site):
        self.model_class=model_class
        self.site=site
        self.request=None
        self.app_label=model_class._meta.app_label
        self.model_name=model_class._meta.model_name


    def get_add_or_edit_model_form(self):
        if self.add_or_edit_model_form:
            return self.add_or_edit_model_form
        else:
            #对象由类创建，类由type创建
            from django.forms import ModelForm
            # class MyModelForm(ModelForm):
            #     class Meta:
            #         model = self.model_class
            #         fields = "__all__"
            # return MyModelForm
            _m=type('Meta',(object,),{'model':self.model_class,'fields':'__all__'})
            MyModelForm=type('MyModelForm',(ModelForm,),{'Meta':_m})
            return MyModelForm


    def get_model_field_name_list(self):
        """
        获取当前model中定义的字段
        :return:
        """
        # print(type(self.model_class._meta))
        from django.db.models.options import Options
        return [item.name for item in self.model_class._meta.fields]

    def another_urls(self):
        """
        钩子函数，用于自定义额外的url
        :return:
        """
        return []

    def changelist_param_url(self, query_params=None):
        # redirect_url = "%s?%s" % (reverse('%s:%s_%s' % (self.site.namespace, self.app_label, self.model_name)),
        #                           urllib.parse.urlencode(self.change_list_condition))
        if query_params:
            redirect_url = "%s?%s" % (
                reverse('%s:%s_%s_changelist' % (self.site.namespace, self.app_label, self.model_name)),
                query_params.urlencode())
        else:
            redirect_url=reverse('%s:%s_%s_changelist' % (self.site.namespace, self.app_label, self.model_name))
        return redirect_url

    @property
    def urls(self):
        from django.conf.urls import url
        info=self.model_class._meta.app_label,self.model_class._meta.model_name
        urlpatterns = [
            url(r'^$', self.changelist_view, name='%s_%s_changelist' % info),
            url(r'^add/$', self.add_view, name='%s_%s_add' % info),
            url(r'^(.+)/delete/$', self.delete_view, name='%s_%s_delete' % info),
            url(r'^(.+)/change/$', self.change_view, name='%s_%s_change' % info),
            url(r'^(.+)/detail/$', self.detail_view, name='%s_%s_detail' % info),
            # For backwards compatibility (was the change url before 1.9)
            # url(r'^(.+)/$', RedirectView.as_view(pattern_name='%s:%s_%s_change' % ((self.backend_site.name,) + info))),
        ]
        urlpatterns+=self.another_urls()
        return urlpatterns

    def changelist_view(self,request):
        """
        查看列表
        :param requset:
        :return:
        """
        #生成页面上的添加按钮
        #namespace，app_label,model_name

        # print(request.GET.urlencode()) #urlencode获取url
        param_dict=QueryDict(mutable=True) #设置为可修改
        if request.GET:
            param_dict['_changlistfilter']=request.GET.urlencode()
        base_add_url = reverse("{2}:{0}_{1}_add".format(self.app_label, self.model_name, self.site.namespace))
        add_url="{0}?{1}".format(base_add_url,param_dict.urlencode())


        self.request=request
        #分页开始
        condition={}
        from extraapp.utils.my_page import PageInfo
        all_count=self.model_class.objects.filter(**condition).count()
        base_page_url=self.changelist_param_url()
        page_param_dict=copy.deepcopy(request.GET) #全新的复制一份
        page_param_dict._mutable=True
        page_param_dict["page"]=1
        page_obj=PageInfo(request.GET.get("page"),all_count,base_page_url,page_param_dict)
        result_list=self.model_class.objects.filter(**condition)[page_obj.start:page_obj.end]

       ################ Action操作 ################
        #get请求，显示下拉框
        action_list=[]
        for item in self.action_list:
            tpl={'name':item.__name__,'text':item.text}
            action_list.append(tpl)
        if request.method=="POST":
            """1、获取action"""
            func_name_str=request.POST.get('action')
            ret=getattr(self,func_name_str)(request)

            action_page_url=self.changelist_param_url()
            if ret:
                action_page_url=self.changelist_param_url(request.GET)
            return redirect(action_page_url)
        ######组合搜索操作#######
        from extraapp.utils.filter_code import FilterList
        filter_list=[]
        for option in self.filter_list:
            if option.is_func:
                data_list=option.field_or_func(self,option,request)
            else:
                #username ug m2m
                from django.db.models import ForeignKey,ManyToManyField
                field=self.model_class._meta.get_field(option.field_or_func)
                # print(request.GET)
                if isinstance(field,ForeignKey):
                    # print(field.rel.model) #封装了外键表对象
                    data_list=FilterList(option,field.rel.model.objects.all(),request)
                elif isinstance(field,ManyToManyField):
                    data_list = FilterList(option,field.rel.model.objects.all(), request)
                else:
                    # self.model_class or field.model 都可以拿到userinfo
                    data_list = FilterList(option,field.model.objects.all(), request)
            # yield data_list
            filter_list.append(data_list)

        context={
            'result_list':result_list,
            'list_display':self.list_display,
            'BaseExtraAdmin_obj':self,
            'add_url':add_url,
            'page_str':page_obj.pager(),
            'action_list':action_list,
            'filter_list':filter_list

        }
        return render(request, 'exapp/change_list.html',
                      # {'result_list':result_list,'list_display':self.list_display}
                        context #同上一样
                      )

    def add_view(self,request):
        """
        添加数据
        :param request:
        :return:
        """
        if request.method=="GET":
            # print(request.GET.get("_changlistfilter"))
            model_form_obj=self.get_add_or_edit_model_form()()
            context = {
                'form': model_form_obj
            }
            return render(request, 'exapp/add.html', context)

        else:
            model_form_obj = self.get_add_or_edit_model_form()(data=request.POST,files=request.FILES)
            if model_form_obj.is_valid():
                obj=model_form_obj.save()
                #如果是popup，关闭页面，并把数据返回给调用者，
                popid=request.GET.get('popup')
                if popid:
                    return render(request, 'exapp/popup_response.html',{ 'data_dict':{'pk': obj.pk,'text': str(obj),'popid': popid}})

                else:
                    #否则添加成功进行跳转
                    # base_list_url = reverse(
                    #     "{2}:{0}_{1}_changelist".format(self.app_label, self.model_name, self.site.namespace))
                    base_list_url=self.changelist_param_url()
                    list_url = "{0}?{1}".format(base_list_url, request.GET.get("_changlistfilter"))
                    return redirect(list_url)

            context = {
                'form': model_form_obj
            }
            return render(request,'exapp/add.html',context)


    def delete_view(self,request,pk):
        """
        删除数据
        :param request:
        :param pk:
        :return:
        """
        """
        根据pk获取数据，然后delete()
        获取url，跳转回列表页面
        """
        self.model_class.objects.filter(pk=pk).delete()
        _changlistfilter=request.GET.get('_changlistfilter')
        # redirect_url = reverse('%s:%s_%s_changelist' % (self.site.namespace, self.app_label, self.model_name))
        redirect_url = self.changelist_param_url()
        if _changlistfilter:
            change_list_url="%s?%s"%(redirect_url,_changlistfilter)
        else:
            change_list_url= redirect_url
        return redirect(change_list_url)

    def change_view(self,request,pk):
        """
        修改数据
        :param request:
        :param pk:
        :return:
        """
        #1、获取_changelistfilter中传递的参数
        #request.GET.get("_changlistfilter")
        #2、页面显示并提供默认值ModelForm
        obj=self.model_class.objects.filter(pk=pk).first()
        if not obj:
            return HttpResponse("id不存在")
        if request.method=="GET":
            model_form_obj=self.get_add_or_edit_model_form()(instance=obj) #instance会更新
        else:
            model_form_obj = self.get_add_or_edit_model_form()(data=request.POST,files=request.FILES,instance=obj) #成功
            if model_form_obj.is_valid():
                model_form_obj.save()
            base_list_url=self.changelist_param_url()
            request_parameters=request.GET.get("_changlistfilter")
            if request_parameters:
                list_url = "%s?%s"%(base_list_url,request_parameters)
            else:
                list_url=base_list_url
            return redirect(list_url)
        # 3、返回页面
        context={
            'form':model_form_obj
        }

        return render(request,'exapp/edit.html',context)

    def detail_view(self, request, pk):
        """
        查看详细
        :param request:
        :param pk:
        :return:
        """
        row = self.model_class.objects.filter(pk=pk).first()
        fields = self.get_add_or_edit_model_form().Meta.fields
        if fields == '__all__':
            fields = self.get_model_field_name_list()
            # print(self.get_model_field_name_list_m2m())
        for name in fields:
            val = getattr(row, name)
            # print(name, val)

        context = {
            'row': row
        }
        #页面优先级
        return TemplateResponse(request, self.change_form_template or [
            'exapp/%s/%s/detail.html' % (self.app_label, self.model_name),
            'exapp/%s/detail.html' % self.app_label,
            'exapp/detail.html'
        ], context)



class ExtraAppSite(object):
    def __init__(self):
        self._registry={}
        self.namespace="extraapp"
        self.app_name="extraapp"

    def register(self,model_class,xxx=BaseExtraAdmin):
        self._registry[model_class]=xxx(model_class,self)
        """
        app01下面是UserInfo
        {
            UserInfo类:BaseExtraAdmin(UserInfo类,ExtraAppSite对象) ExtraAppUserInfo对象,都是同一个site实例
            Role类:BaseExtraAdmin(Role类,ExtraAppSite对象)
            XX类:BaseExtraAdmin(XX类,ExtraAppSite对象)
        }
        """

    def get_urls(self):
        from django.conf.urls import url, include
        ret=[
            url(r'^$', self.index, name='index'),
            url(r'^login/',self.login,name='login'),
            url(r'^logout/',self.logout,name='logout')
        ]
        for model_cls,extraapp_admin_obj in self._registry.items():
            app_label=model_cls._meta.app_label
            model_name=model_cls._meta.model_name
            # print(extraapp_admin_obj)
            #<class 'app01.models.Role'> app01 role
            # print(model_cls,app_label,model_name)
            ret.append(url(r'^%s/%s/'%(app_label,model_name), include(extraapp_admin_obj.urls)))
        return ret

    @property
    def urls(self):
        return (self.get_urls(),self.app_name,self.namespace)


    def login(self, request):
        """
        用户登录
        :param request:
        :return:
        """

        if request.method == 'GET':
            return render(request, 'login.html')
        else:
            from extraapp import models
            from extraapp.server_model import rbac

            user = request.POST.get('username')
            pwd = request.POST.get('password')
            obj = models.User.objects.filter(username=user, password=pwd).first()
            if obj:
                request.session['user_info']={'nid':obj.pk,'username':obj.username}
                rbac.initial_permission(request, obj)
                return redirect('/exapp/')
            else:
                return render(request, 'login.html')

    def logout(self, request):
        """
        用户注销
        :param request:
        :return:
        """
        pass

    def index(self, request):
        """
        首页
        :param request:
        :return:
        """
        return render(request, 'exapp/index.html')

#单例模式
site=ExtraAppSite()