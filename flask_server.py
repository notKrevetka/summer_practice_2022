from flask import Flask, render_template, request, make_response, session, redirect
import db_logic
import os
import json
import re

server_object = Flask(__name__)


@server_object.route('/login.html', methods=['GET', 'POST'])
def login():
    session['is_logged_in'] = False
    session['login'] = " "

    if request.method == 'GET':
        return render_template('login.html')

    user_login, user_password = request.form['login'], request.form['password']
    such_users = db_logic.count_users_with_such_login(user_login)
    print('ПОЛЬЗОВАТЕЛЕЙ С ТАКИМ ЛОГИНОМ', such_users)
    if such_users != 0:
        true_password = db_logic.get_password_by_login(user_login)
        if true_password == user_password:
            session['is_logged_in'] = True
            session['login'] = user_login
            return redirect('/cabinet.html')
        return render_template('login.html', wrong_password=True)
    return render_template('login.html', wrong_login=True)


@server_object.route('/registration.html', methods=['GET', 'POST'])
def registration():
    if request.method == 'GET':
        return render_template('registration.html')
    new_login, new_password, password_check = request.form[
        'login'], request.form['password'],  request.form['password_check']
    such_users = db_logic.count_users_with_such_login(new_login)
    if such_users == 0:
        if new_password == password_check:
            db_logic.add_user(new_login, new_password)
            session['is_logged_in'] = True
            session['login'] = new_login
            return redirect('/cabinet.html')
        else:
            return render_template('registration.html', wrong_password=True)
    true_password = db_logic.get_password_by_login(new_login)
    if true_password == new_password and true_password == password_check:
        session['is_logged_in'] = True
        session['login'] = new_login
        return redirect('/cabinet.html')
    return render_template('registration.html', wrong_password=True)


@server_object.route('/lecture_<lecture_num>.html', methods=['GET', 'POST'])
def lecture(lecture_num):
    return render_template(f'/lectures/lecture_{lecture_num}.html', lecture_num=int(lecture_num), lectures_total_num=len(os.listdir('templates/lectures')))


@server_object.route('/test_<test_num>.html', methods=['GET', 'POST'])
def test(test_num):
    if request.method == 'GET':
        with open('test_content.json', 'r', encoding='utf-8') as f:
            all_test_obj = json.load(f)
            all_tests_list = all_test_obj["tests"]
            this_test = all_tests_list[int(test_num)-1]
            print(this_test, test_num)
        return render_template('/test_base.html', test_num=int(test_num), this_test=this_test)


@server_object.route('/cabinet.html', methods=['GET', 'POST'])
def cabinet_content():
    lectures_list = os.listdir('templates/lectures')
    titles = []
    for name in lectures_list:
        with open(f'templates/lectures/{name}', 'r') as f:
            text = f.read()
        title = re.search(r'<title>(.*)</title>', text).groups()[0]
        titles.append(title)
    each_test_results = db_logic.get_user_answers(session['login'])
    each_test_results= dict(sorted(zip(each_test_results.keys(), each_test_results.values())))
    print(each_test_results)
    return render_template('/cabinet.html',
                           lectures_total_num=len(os.listdir('templates/lectures')),
                           lectures_list=zip(lectures_list, titles),
                           tests_results=each_test_results)


@server_object.route('/add_test_result', methods=['POST'])
def add_test_result():
    db_logic.add_test_try_result(
        request.form['login'], request.form['test_num'], request.form['result'],)

    return "200"


if __name__ == '__main__':
    server_object.secret_key = 'abc'
    server_object.run(debug=True)
