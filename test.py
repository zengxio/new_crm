# #!/usr/bin/env python
# #encoding:utf-8
# class Foo():
#
#
#     def get_urls(self):
#         # print(self.add)
#         # print(self.delete)
#         ret=[self.add,self.delete]
#         return ret
#
#     @property
#     def urls(self):
#         return self.get_urls()
#
#
#     def add(self):
#        return "add"
#
#     def delete(self):
#         return "delete"
#
# f=Foo()
# for i in f.urls:
#     print(i())

#单例模式
#方法1 模块导入
# site=ExtraAppSite()

#方法2类方法
# class Foo():
#     _instance=None
#     def __init__(self):
#         pass
#     @classmethod
#     def get_instance(cls):
#         if cls._instance:
#             return cls._instance
#         else:
#             obj=cls()
#             cls._instance=obj
#             return obj
# a1=Foo.get_instance()

#方法3__new__
# class Foo():
#     _instance=None
#     def __init__(self):
#         pass
#
#     def __new__(cls, *args, **kwargs): #创建对象
#         if cls._instance:
#             return cls._instance
#         else:
#             obj=object.__new__(cls, *args, **kwargs) #创建出来的对象传给init self里面
#             cls._instance=obj
#         return obj
#
#  #用户行为不需要改变
# obj=Foo()
# obj1=Foo()
# print(obj)
# print(obj1)

#单例模式的用处
    # 自定义CURD组件时，没有必要创建多个实例来浪费空间
    # 发布文章，对于特殊字符的过滤KindEditor
        # class Kind():
        #     def __init__(self):
        #         self.valid_tags=[
        #             "a","div","h1"
        #         ]
        #     def valid(self,content):
        #         pass
        # obj=Kind()
        # body=obj.valid("<html>")


#封装思想
#封装类中封装了数据，方法
#职责划分：封装什么就处理什么，目的为其他调用者提供功能
class Foo():
    def __init__(self,name,age):
        self.name=name
        self.age=age

    @property
    def bs(self):
        if self.age>15:
            return "old"
        else:
            return "new"

    def nick(self):
        tpl=self.name+self.age
        return tpl

class Bar():
    def __init__(self,option,attr):
        self.option=option
        self.attr=attr

    def __iter__(self):
        yield "全部："
        for i in self.attr:
            yield "<a href='{0}'>{1}</a>".format(i,self.option.bs+i)


    def show(self):
        self.option.nick()

obj_list=[
    Bar(Foo('曾小燕',18,),['学习','睡觉','运动']),
    Bar(Foo('小曾燕',18,),['学习','睡觉','运动']),
    Bar(Foo('燕小曾',18,),['学习','睡觉','运动']),

]
for row in obj_list:

    for item in row:
        print(item,end=" ")
    else:
        print("")



