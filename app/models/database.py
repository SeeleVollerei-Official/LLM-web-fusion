from datetime import datetime, timedelta


class MockDatabase:
    def __init__(self):
        self.users = {}  # 一级目录，存储用户账号和密码
        self.active_user = None  # 当前激活的用户
        self.expense_categories = ['餐饮', '娱乐', '交通', '购物', '其他']  # 消费类别

    def add_user(self, username, password, email, phone, monthly_income, monthly_savings_goal):
        """
        添加用户
        :param monthly_savings_goal:
        :param monthly_income:
        :param email:
        :param phone:
        :param username: 用户名
        :param password: 密码
        """
        if username in self.users:
            raise ValueError("User already exists")
        self.users[username] = {
            'password': password,
            'profile': {
                'username': username,
                'email': email,
                'phone': phone,
                'monthly_income': monthly_income,
                'monthly_savings_goal': monthly_savings_goal,
                'total_savings': 0.0
            },
            'expenses': [],  # 消费记录列表
            'category_totals': {category: 0.0 for category in self.expense_categories},  # 类别总金额记录
            'monthly_saving': []  # 月份和对应月的节约金额列表
        }

    def update_profile(self, **kwargs):
        """
        修改用户的个人资料内容
        :param username: 用户名
        :param password: 密码
        :param kwargs: 要更新的个人资料字段和值
        """
        if self.active_user:
            profile = self.get_profile()
            for key, value in kwargs.items():
                if key in profile:
                    profile[key] = value

    def add_expense(self, expense):
        """
        添加消费记录
        :param expense: 消费记录字典，包含消费时间、消费金额和消费内容
        """
        if self.active_user:
            category = expense.get('category', '其他')
            if category in self.expense_categories:
                self.active_user['expenses'].append(expense)
                self.active_user['category_totals'][category] += expense['amount']
                self.active_user['profile']['total_savings'] -= expense['amount']

    def delete_expense(self, expense_index):
        """
        删除消费记录
        :param expense_index: 要删除的消费记录的索引
        """
        if self.active_user and 0 <= expense_index < len(self.active_user['expenses']):
            expense = self.active_user['expenses'][expense_index]
            category = expense.get('category', '其他')
            if category in self.expense_categories:
                self.active_user['category_totals'][category] -= expense['amount']
                self.active_user['profile']['total_savings'] += expense['amount']
                del self.active_user['expenses'][expense_index]

    def get_profile(self):
        """
        返回当前激活用户的个人资料
        :return: 用户的个人资料字典
        """
        if self.active_user:
            return self.active_user['profile']
        return None

    def get_expenses(self, month=None):
        """
        返回指定月份的消费记录
        :param month: 年月字符串（格式为 "YYYY-MM"），如果为 None，则返回所有消费记录
        :return: 指定月份的消费记录列表
        """
        if self.active_user:
            if month is None:
                return self.active_user['expenses']
            else:
                return [expense for expense in self.active_user['expenses'] if expense['time'].strftime('%Y-%m') == month]
        return []

    def get_category_totals(self, month):
        """
        返回指定月份的不同类别的消费情况
        :param month: 年月字符串（格式为 "YYYY-MM"）
        :return: 指定月份不同类别的消费情况字典
        """
        if self.active_user:
            category_totals = {category: 0.0 for category in self.expense_categories}
            for expense in self.active_user['expenses']:
                expense_month = expense['time'].strftime('%Y-%m')
                if expense_month == month:
                    category = expense.get('category', '其他')
                    if category in self.expense_categories:
                        category_totals[category] += expense['amount']
            return category_totals
        return {}

    def update_monthly_saving(self):
        """
        按月份计算并更新节约金额
        """
        if self.active_user:
            profile = self.active_user['profile']
            expenses = self.active_user['expenses']
            monthly_income = profile['monthly_income']

            # 创建一个字典来存储每个月的总消费
            monthly_expenses = {}
            for expense in expenses:
                month = expense['time'].strftime('%Y-%m')  # 获取消费记录的年月
                if month not in monthly_expenses:
                    monthly_expenses[month] = 0.0
                monthly_expenses[month] += expense['amount']

            # 计算每个月的节约金额并更新monthly_saving列表
            self.active_user['monthly_saving'] = [
                {
                    'month': month,
                    'saving': monthly_income - total_expense
                }
                for month, total_expense in monthly_expenses.items()
            ]

    def get_saving_for_month(self, month):
        """
        返回指定月份的节约金额
        :param month: 年月字符串（格式为 "YYYY-MM"）
        :return: 指定月份的节约金额
        """
        self.update_monthly_saving()
        if self.active_user:
            for saving in self.active_user['monthly_saving']:
                if saving['month'] == month:
                    return saving['saving']
        return None

    def get_account_balance(self):
        """
        返回账户余额，账户余额的计算方式是将所有的节约余额相加
        :return: 账户余额
        """
        self.update_monthly_saving()
        if self.active_user:
            total_savings = sum(saving['saving'] for saving in self.active_user['monthly_saving'])
            return total_savings
        return 0.0

    def get_daily_expenses_for_month(self, time):
        """
        返回指定月份每五天的支出
        :param time: 年月字符串（格式为 "YYYY-MM"）
        :return: 指定月份每五天的支出字典
        """
        if self.active_user:
            five_day_expenses = {}
            expenses = [expense for expense in self.active_user['expenses'] if
                        expense['time'].strftime('%Y-%m') == time]

            # 找到月份的第一天和最后一天
            first_day = datetime.strptime(time + '-01', '%Y-%m-%d')
            last_day = first_day.replace(day=28) + timedelta(days=4)  # 找到下个月的第四天
            last_day = last_day - timedelta(days=last_day.day)  # 找到这个月的最后一天

            # 初始化五天周期的起始日期
            start_date = first_day
            while start_date <= last_day:
                end_date = start_date + timedelta(days=4)
                period = (start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))
                five_day_expenses[period] = 0.0

                # 计算该周期内的总支出
                for expense in expenses:
                    if start_date <= expense['time'] <= end_date:
                        five_day_expenses[period] += expense['amount']

                # 移动到下一个五天周期
                start_date = end_date + timedelta(days=1)

            return five_day_expenses
        return {}

    def check_user_credentials(self, username, password):
        """
        检查用户名和密码是否正确，并设置当前激活用户
        :param username: 用户名
        :param password: 密码
        :return: 布尔值，表示用户存在且密码正确
        """
        user = self.users.get(username)
        if user and user['password'] == password:
            self.active_user = user
            return True
        return False
