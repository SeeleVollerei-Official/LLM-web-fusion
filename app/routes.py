from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import re

from app.models.database import MockDatabase
from app.models.image2text import image2text
from app.models.LLMapi import analyse_response
from config import default_display_settings

app = Flask(__name__)
CORS(app)  # 启用CORS支持
app.secret_key = 'your-secret-key'  # 用于session加密
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super(CustomJSONEncoder, self).default(obj)


app.json_encoder = CustomJSONEncoder


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    credentials_valid = db.check_user_credentials(username, password)

    if credentials_valid:
        return jsonify({"user": username}), 200
    else:
        return jsonify({"error": "Invalid username or password"}), 401


@app.route('/api/profile', methods=['GET'])
def get_profile():
    profile_data = db.get_profile()

    if profile_data is None:
        return jsonify({'error': 'Profile not found'}), 404

    response_data = {
        'username': profile_data.get('username', ''),
        'email': profile_data.get('email', ''),
        'phone': profile_data.get('phone', ''),
        'monthlyIncome': profile_data.get('monthly_income', 0.0),
        'monthlyBudget': profile_data.get('monthly_savings_goal', 0.0)
    }

    return jsonify(response_data), 200


@app.route('/api/profile/modification', methods=['PUT'])
def revise_profile():
    profile_data = request.get_json()

    username = profile_data.get('username')
    email = profile_data.get('email')
    phone = profile_data.get('phone')
    monthly_income = profile_data.get('monthlyIncome')
    monthly_savings_goal = profile_data.get('monthlyBudget')
    db.update_profile(username=username, email=email, phone=phone,
                      monthly_income=float(monthly_income), monthly_savings_goal=float(monthly_savings_goal))

    return jsonify({'message': 'Success'}), 200


@app.route('/api/index/categories', methods=['GET'])
def get_index_categories_ifo():
    now = datetime.now()
    category_totals = db.get_category_totals(str(now.year) + '-' + str(now.month))
    if category_totals is None:
        return jsonify({'error': 'Category not found'}), 404

    food = category_totals.get('餐饮', 0.0)
    entertainment = category_totals.get('娱乐', 0.0)
    transport = category_totals.get('交通', 0.0)
    shopping = category_totals.get('购物', 0.0)
    other = category_totals.get('其他', 0.0)

    response_data = {
        'food': food,
        'entertainment': entertainment,
        'transport': transport,
        'shopping': shopping,
        'other': other,
        'total': food + entertainment + transport + shopping + other
    }

    return jsonify(response_data), 200


@app.route('/api/index/mainInfo', methods=['GET'])
def get_index_main_ifo():
    username = db.get_profile()['username']
    savings = db.get_account_balance()  # 账户余额
    income = db.get_profile()['monthly_income']
    goal = db.get_profile()['monthly_savings_goal']

    now = datetime.now()
    last_month_savings = db.get_saving_for_month(str(now.year) + '-' + str(now.month - 1))

    response_data = {
        'username': username,
        'savings': savings,
        'income': income,
        'goal': goal,
        'lastMonthSavings': last_month_savings,
        'isAchieved': last_month_savings > goal
    }

    return jsonify(response_data), 200


@app.route('/api/index/analysis', methods=['GET'])
def get_expense_data_for_analysis():
    now = datetime.now()
    category_totals = db.get_category_totals(str(now.year) + '-' + str(now.month))
    profile_data = db.get_profile()

    food = category_totals.get('餐饮', 0.0)
    entertainment = category_totals.get('娱乐', 0.0)
    transport = category_totals.get('交通', 0.0)
    shopping = category_totals.get('购物', 0.0)
    other = category_totals.get('其他', 0.0)
    total = food + entertainment + transport + shopping + other
    average = total / 30

    monthly_income = profile_data.get('monthly_income')
    monthly_savings_goal = profile_data.get('monthly_savings_goal')
    proportion = total / (monthly_income - monthly_savings_goal)

    now = datetime.now()
    daily_data = db.get_daily_expenses_for_month(str(now.year) + '-' + str(now.month))
    if len(daily_data) == 7:
        # 分别将六个周期的数据保存到六个变量中
        period1, period2, period3, period4, period5, period6, period7 = daily_data.keys()
        expense1 = daily_data[period1]
        expense2 = daily_data[period2]
        expense3 = daily_data[period3]
        expense4 = daily_data[period4]
        expense5 = daily_data[period5]
        expense6 = daily_data[period6]
        expense7 = daily_data[period7]
    else:
        expense1 = expense2 = expense3 = expense4 = expense5 = expense6 = expense7 = 0

    response_data = {
        'total': total,
        'average': average,
        'proportion': proportion,
        'period1': expense1,
        'period2': expense2,
        'period3': expense3,
        'period4': expense4,
        'period5': expense5,
        'period6': expense6,
        'period7': expense7
    }

    return jsonify(response_data), 200


@app.route('/api/record/upload', methods=['POST'])
def upload_file():
    # 检查是否有文件在请求中
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    # 如果用户没有选择文件，浏览器也会提交一个没有文件名的空部分
    if file.filename == '':
        return 'No selected file'
    if file and allowed_file(file.filename):
        filename = file.filename
        file.save(f'../save/{filename}')

        question_part1 = '你是一个消费统计工具。作为消费统计工具，在从消费记录中提取内容时你应当遵守以下守则。' \
                         '你的回答包括4个内容：消费内容,消费金额,消费时间,消费类别。' \
                         '消费时间包含年月日，消费时间的输出格式：\'\'\'xxxx-xx-xx\'\'\'' \
                         '消费内容是几个字符的中文或英文，不可能是一串数字或字母。' \
                         '消费金额以负号开始，是一个带有二位小数的负浮点数，位置出现在消费时间以前。' \
                         '消费类别只包括:\'\'\'餐饮\'\'\'、\'\'\'娱乐\'\'\'、\'\'\'交通\'\'\'、\'\'\'购物\'\'\'和\'\'\'其他\'\'\'五种类型。在餐饮店消费属于餐饮，不属于购物。网购食品属于购物，不属于餐饮。' \
                         '回答时只能回答消费内容、消费金额、消费时间和消费类别，不能包含其他无关内容。' \
                         '例如，你的回答可以是：\'\'\'消费内容:必胜客;消费金额:100.00;消费时间:2021-02-18;消费类别:餐饮\'\'\'' \
                         '以下是我的一个消费记录，请按照守则从中提取消费内容、消费金额、消费时间和消费类别。'

        question_part2 = '消费记录：###' + image2text(filename) + '###'
        question = question_part1 + question_part2
        answer = analyse_response(question)

        parts = answer.split(';')
        result = {}
        for part in parts:
            key, value = part.split(':', 1)
            key = key.strip()
            value = value.strip()
            if key == '消费内容':
                result['content'] = value
            elif key == '消费金额':
                result['amount'] = value
            elif key == '消费时间':
                result['time'] = value
            elif key == '消费类别':
                result['category'] = value

        db.add_expense({
            'time': datetime.strptime(result['time'], "%Y年%m月%d日%H:%M:%S"),
            'amount': abs(float(result['amount'])),
            'content': result['content'],
            'category': result['category']
        })
        print('add_expense_success')

        return jsonify({'message': 'Success'}), 200
    else:
        return jsonify({"error": "Invalid file"}), 401


@app.route('/api/record/analysis', methods=['GET'])
def LLM_data_analysis():
    now = datetime.now()
    question_part1 = '你是一个个人消费管理助手，下面我将提供我在本月和上月的消费记录，请分析本月之于上月我的消费变化情况，并回答我我应该减少哪些方面的不必要支出以满足我的节约目标'
    question_part2 = '我的上月消费记录如下：###' + str(db.get_category_totals(str(now.year) + '-' + str(now.month - 1))) + '###'
    question_part3 = '我的本月消费记录如下：###' + str(db.get_category_totals(str(now.year) + '-' + str(now.month))) + '###'

    question = question_part1 + question_part2 + question_part3
    answer = analyse_response(question)

    markdown_patterns = [
        r'\*+',  # 匹配星号
        r'_+',  # 匹配下划线
        r'\#+',  # 匹配井号
        r'\[.*?\]',  # 匹配方括号及其内容
        r'\(.*?\)',  # 匹配括号及其内容
        r'`+',  # 匹配反引号
        r'~+',  # 匹配波浪号
        r'>+',  # 匹配大于号
    ]

    # 合并所有模式
    combined_pattern = '|'.join(markdown_patterns)

    # 使用正则表达式替换所有Markdown控制符
    cleaned_text = re.sub(combined_pattern, '', answer)

    return jsonify({'message': cleaned_text}), 200


@app.route('/api/records', methods=['POST'])
def get_expense_data_to_display():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    month = data.get('month')
    now = datetime.now()
    data = db.get_expenses(str(now.year)+'-'+str(month))

    return jsonify(data), 200


if __name__ == '__main__':
    db = MockDatabase()
    default_display_settings(db)
    app.run(debug=True)
