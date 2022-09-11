from flask import Flask, render_template, request, make_response, session
import db_logic
import os
import json

server_object = Flask(__name__)


@server_object.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@server_object.route('/page2.html', methods=['GET', 'POST'])
def give_page2():
    return '<h1>page2</h1>'


@server_object.route('/show_template.html', methods=['GET', 'POST'])
def show_template():
    if request.method == 'GET':
        vremya_stroka = asctime()
        return render_template('show_template.html', time_param=vremya_stroka)


@server_object.route('/login.html', methods=['GET', 'POST'])
def login():
    session['is_logged_in'] = False
    session['login'] = None
    if request.method == 'GET':
        return render_template('login.html')

    user_login, user_password = request.form['login'], request.form['password']

    such_users = db_logic.count_users_with_such_login(user_login)
    if such_users != 0:
        true_password = db_logic.get_password_by_login(user_login)

        if true_password == user_password:
            session['is_logged_in'] = True
            session['login'] = user_login
            return render_template('content_lectures.html', lectures_list=os.listdir('templates/lectures'))
        return render_template('login.html', wrong_password=True)

    return render_template('login.html', wrong_login=True)


@server_object.route('/registration.html', methods=['GET', 'POST'])
def registration():
    if request.method == 'GET':
        return render_template('registration.html')

    new_login, new_password, password_check = request.form['login'], request.form['password'],  request.form['password_check']

    such_users = db_logic.count_users_with_such_login(new_login)

    if such_users == 0:
        if new_password == password_check:
            db_logic.add_user(new_login, new_password)
            session['is_logged_in'] = True
            session['login'] = new_login
            return render_template('content_lectures.html', lectures_list=os.listdir('templates/lectures'))
        else:
            return render_template('registration.html', wrong_password=True)

    true_password = db_logic.get_password_by_login(new_login)
    if true_password == new_password and true_password == password_check:
        session['is_logged_in'] = True
        session['login'] = new_login
        return render_template('content_lectures.html', lectures_list=os.listdir('templates/lectures'))

    return render_template('registration.html', wrong_password=True)


@server_object.route('/lecture_<lecture_num>.html', methods=['GET', 'POST'])
def lecture(lecture_num):
    return render_template(f'/lectures/lecture_{lecture_num}.html', lecture_num=int(lecture_num), lectures_total_num=len(os.listdir('templates/lectures')))


@server_object.route('/content_lectures.html', methods=['GET', 'POST'])
def lectures_table_of_contents():
    return render_template('/content_lectures.html', lectures_list=os.listdir('templates/lectures'))


@server_object.route('/test_<test_num>.html', methods=['GET', 'POST'])
def test(test_num):
    with open('test_content.json', 'r', encoding='utf-8') as f:
        all_test_obj = json.load(f)
        all_tests_list = all_test_obj["tests"]
        this_test = all_tests_list[int(test_num)-1]
        print(this_test, test_num)
    return render_template('/test_base.html', test_num=int(test_num), this_test=this_test)


@server_object.route('/content_tests.html', methods=['GET', 'POST'])
def lectures_table_of_tests():
    return render_template('/content_tests.html', lectures_total_num=len(os.listdir('templates/lectures')))










if __name__ == '__main__':
    server_object.secret_key = 'abodwdfebtgta'
    server_object.run(debug=True)
