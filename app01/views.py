from django.shortcuts import render,HttpResponse
# from django.urls import reverse
# # Create your views here.
# from django.forms import Form
# from django.forms.models import ModelMultipleChoiceField,ModelChoiceField
# from django.forms import fields
# from django.forms import widgets
from app01 import models
#
# # class TestForm(Form):
# #     user=fields.CharField()
# #     group=fields.ChoiceField(choices=[])
# #     def __init__(self,*args,**kwargs):
# #         super(TestForm,self).__init__(*args,**kwargs)
# #         self.fields['group'].choices=models.UserGroup.objects.values_list("id","title")
#
# class TestForm(Form):
#     user = fields.CharField()
#     # group=ModelChoiceField(queryset=models.UserGroup.objects.all())  #也可以实现动态显示数据，但是他依赖model 中的__str__
#     group=ModelMultipleChoiceField(queryset=models.UserGroup.objects.all())
#
# def test(request):
#     # #反向生成URL,
#     # # include导入其他文件路径，include('app01.urls',namespace='aaa')#
#     # #app01.urls
#     #     #aaa:login
#     # #  如果分发的时候指定了include,和namesapce，需要加上namesapce。为了解决name冲突
#     # url=reverse("extraapp:login")
#     # print(url)
#     # return HttpResponse("...")
#     # url = reverse("extraapp:app01_userinfo_add")
#     # print(url)
#     form=TestForm()
#     if form:
#         return render(request,'test.html',{'form':form})
#
#
# def ttt(request):
#     url = reverse("tt")
#     print(url)
#     return HttpResponse("...")

def test(request):
    user_group_list=models.UserGroup.objects.all()
    return render(request, '临时存放/test.html', {'user_group_list':user_group_list})

def add_test(request):
    if request.method=="GET":
        return render(request, '临时存放/add_test.html')
    else:
        popid=request.GET.get("popup")
        if popid:
            title=request.POST.get("title")
            obj=models.UserGroup.objects.create(title=title)
            return render(request, '临时存放/popup_response.html', {'id':obj.id, 'title':obj.title, 'popid':popid})
        else:
            title=request.POST.get('title')
            models.UserGroup.objects.create(title=title)
            return HttpResponse('重定向列表页面:所有数据')