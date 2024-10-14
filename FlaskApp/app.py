import json
import mypackage
from flask import Flask, render_template, request, flash, redirect, url_for

from flask_login import LoginManager, login_required, logout_user, current_user, login_user

app = Flask(__name__)
app.secret_key = 'hardkey!'
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    try:
        user_type, id_ = user_id.split('_')
        user = mypackage.db_utils.User.get_user_by_id(id_, user_type)
        return user
    except Exception as e:
        print(e)
        return None



@app.route("/")
def Main():
    return render_template('index.html', context="/")


@app.route("/templates/menu.html")
def Menu():
    return render_template('menu.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
        user_type = request.form['user_type']

        user = mypackage.db_utils.User.get_user(login, password, user_type)
        if user:
            login_user(user)
            return redirect(url_for('Main'))
        flash('Invalid username or password')
    return render_template('login.html')

# @app.route('/dashboard')
# @login_required  # Ограничиваем доступ к этой странице для незалогиненных пользователей
# def dashboard():
#     return f'Hello, {current_user.login}! You are logged in as a {current_user.user_type}.'

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('Main'))
@app.route("/teacher")
def Teacher():
    return render_template('teacher.html', context="/teacher")


@app.route("/teacher/students", methods=['POST'])
def List_of_students():  #сделать через 1 запрос
    fio = request.form.get('fio')
    result = mypackage.db_utils.get_class_id_by_teacher_name(fio.split())
    if result == 404:
        return 'Преподавателя с таким фио не существует, либо у него нет класса!', 404
    else:
        result = mypackage.db_utils.get_class_list_by_classid(result[0])
    return result


@app.route("/teacher/subjects", methods=['POST'])
def List_of_subjects():
    jsonFIO = request.get_json()
    fio = jsonFIO['fio']
    result = mypackage.db_utils.get_subjects_by_teacher(fio.split())
    if (len(result) == 0):
        return {"error": "Преподавателя с таким фио не существует, либо он не ведёт предметы!"}, 404
    subjects = [row[0] for row in result]
    jsonRes = {'subjects': subjects}
    return json.dumps(jsonRes)


@app.route("/teacher/grades", methods=['POST'])
def List_of_grades():
    jsonFIO = request.get_json()
    fio = jsonFIO['fio']
    result = mypackage.db_utils.get_grades_by_teacher(fio.split())
    if len(result) == 0:
        return {"error": "Преподавателя с таким фио не существует, либо он не выставлял оценки!"}, 404
    fields = ['name', 'classname', 'subject', 'grade', 'date']
    dicts_data = [dict(zip(fields, values)) for values in result]
    print(dicts_data)
    for i in range(len(dicts_data)):
        dicts_data[i]['date'] = dicts_data[i]['date'].isoformat()
    json_data = json.dumps(dicts_data)
    return json_data


# @app.route("/teacher/add-grade", methods=['POST'])
# def Add_grade():
#     json_data = request.get_json()
#     mypackage.db_utils.Add_grade(json_data)
#     # fio = json_data['fio']
#     # fio = fio.split()
#     # class_name = json_data['classname']
#     # subject = json_data['subject']
#     # grade = json_data['grade']
#     return "test", 200

if __name__ == "__main__":
    app.run()
