class PageInfo(object):
    def __init__(self, current_page, all_count,base_url, page_param_dict, per_page=10,show_page=11):
        """
        :param current_page: 当前页
        :param all_count:   总数据条数
        :param per_page:    以多少条数据分割
        show_page=11  最多显示多少条数据
        """
        try:
            self.current_page = int(current_page)
        except Exception as e:
            self.current_page = 1  # 默认显示第一页

        self.all_count = all_count
        self.per_page = per_page
        self.base_url = base_url
        self.page_param_dict=page_param_dict

        n, m = divmod(self.all_count, self.per_page)  # 如果有余数，页面+1
        if m:
            n = n + 1
        self.all_page = n
        self.show_page = show_page

    @property
    def start(self):  # 开始页码
        return (self.current_page - 1) * self.per_page

    @property
    def end(self):  # 结束页码
        return self.current_page * self.per_page

    def pager(self):  # 生成页码
        page_list = []
        half = int((self.show_page - 1) / 2)  # 为了使页码前后显示5个
        # 如果数据的总分页小于11
        if self.all_page < self.show_page:
            begin = 1  # 为了避免小于11的时候出现页码存在，却没有数据
            stop = self.all_page + 1  # 加1因为range不取最后一个值
        else:
            # 如果当前页小于等于5永远显示1，11页
            if self.current_page <= half:
                begin = 1
                stop = self.show_page + 1
            else:
                if self.current_page + half > self.all_page:  # 如果当前页码加上将要显示的后五个页码大于总共页码
                    begin = self.all_page - self.show_page + 1  # 定住开头显示的页码
                    # begin= self.current_page-5 #显示到最后一页的时候，就不保证显示11个页码了
                    stop = self.all_page + 1
                else:
                    begin = self.current_page - half  # 前五个页码
                    stop = self.current_page + half + 1  # 后五个页码

        if self.current_page <= 1:
            prev = "<li><a>上一页</a></li>"  # 当前页小于等于1，不跳转
        else:
            self.page_param_dict['page']=self.current_page - 1
            prev = "<li><a href='%s?%s'>上一页</a></li>" % (self.base_url,self.page_param_dict.urlencode(),)
        page_list.append(prev)

        for i in range(begin, stop):
            self.page_param_dict['page']=i
            if i == self.current_page:  # 如果选中一个页码，加active属性
                temp = "<li class='active'><a href='%s?%s'>%s</a></li>" % (self.base_url, self.page_param_dict.urlencode(), i)
            else:
                temp = "<li><a href='%s?%s'>%s</a></li>" % (self.base_url, self.page_param_dict.urlencode(), i)
            page_list.append(temp)

        if self.current_page >= self.all_page:  # 当前页大于等于最后一页，不跳转
            nex = "<li><a>下一页</a></li>"
        else:
            self.page_param_dict['page'] = self.current_page + 1
            nex="<li><a href='%s?%s'>下一页</a></li>" % (self.base_url, self.page_param_dict.urlencode(),)

        page_list.append(nex)
        return ''.join(page_list)  # 转换成字符串
