#!/usr/bin/env python
#encoding:utf-8
from django.template import Library
from types import FunctionType
from django.urls import reverse
from django.forms.models import ModelChoiceField
from extraapp.server_model import v1
register=Library()

@register.inclusion_tag("exapp/add_edit_form.html")  #把值给md.html模版文件，将结果返回给change_list.html
def show_add_edit_form(form):
    # html标签
    from_list = []
    for item in form:
        row = {'is_popup': False, 'item': None, 'popup_url': None}
        # print(item.field.label,item.name)
        # isinstance(item.field,ModelMultipleChoiceField)  #

        if isinstance(item.field,
                      ModelChoiceField) and item.field.queryset.model in v1.site._registry:  # 同时都属于父类，所以fk，m2m都是true
            target_app_label = item.field.queryset.model._meta.app_label  # item.field.queryset.model 是models.表名的对象
            target_model_name = item.field.queryset.model._meta.model_name  # 获取表名
            # self.site.namespace
            url_name = "{0}:{1}_{2}_add".format(v1.site.namespace, target_app_label, target_model_name)
            target_url = "{0}?popup={1}".format(reverse(url_name),item.auto_id)
            row['is_popup'] = True
            row['item'] = item
            row['popup_url'] = target_url

        else:
            row['item'] = item
        from_list.append(row)
    return {'form':from_list}

