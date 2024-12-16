from app.models.database import MockDatabase
from datetime import datetime

default_start_time = datetime(2024, 11, 1, 0, 0, 0)


def default_display_settings(db):
    db.add_user('admin', '123456', email='admin@example.com', phone='1234567890',
                monthly_income=5000.0, monthly_savings_goal=1000.0)
    db.check_user_credentials('admin', '123456')
    db.update_profile(category_totals=10000)

    # ----------------------11月------------------------ #
    db.add_expense({
        'time': datetime(2024, 11, 2, 9, 25, 12),
        'amount': 200.0,
        'content': '红旗超市',
        'category': '餐饮'
    })
    db.add_expense({
        'time': datetime(2024, 11, 6, 10, 00, 00),
        'amount': 128.0,
        'content': 'Game',
        'category': '娱乐'
    })
    db.add_expense({
        'time': datetime(2024, 11, 5, 22, 00, 45),
        'amount': 30.0,
        'content': '公交卡',
        'category': '交通'
    })
    db.add_expense({
        'time': datetime(2024, 11, 11, 21, 45, 34),
        'amount': 150.0,
        'content': '天猫商户',
        'category': '购物'
    })
    db.add_expense({
        'time': datetime(2024, 11, 14, 5, 20, 00),
        'amount': 100.0,
        'content': '转账给个人',
        'category': '其他'
    })

    # ----------------------12月------------------------ #
    db.add_expense({
        'time': datetime(2024, 12, 2, 10, 30, 42),
        'amount': 50.0,
        'content': '干锅鸡',
        'category': '餐饮'
    })
    db.add_expense({
        'time': datetime(2024, 12, 4, 20, 30, 00),
        'amount': 100.0,
        'content': '猫眼电影',
        'category': '娱乐'
    })
    db.add_expense({
        'time': datetime(2024, 12, 6, 10, 00, 00),
        'amount': 648.0,
        'content': 'Game',
        'category': '娱乐'
    })
    db.add_expense({
        'time': datetime(2024, 12, 5, 22, 00, 45),
        'amount': 130.0,
        'content': '滴滴打车',
        'category': '交通'
    })
    db.add_expense({
        'time': datetime(2024, 12, 11, 21, 45, 34),
        'amount': 1500.0,
        'content': '天猫商户',
        'category': '购物'
    })
    db.add_expense({
        'time': datetime(2024, 12, 14, 5, 20, 00),
        'amount': 200.0,
        'content': '转账给个人',
        'category': '其他'
    })
