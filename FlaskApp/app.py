import json
import mypackage
from flask import Flask, render_template, request, flash, redirect, url_for
from configparser import ConfigParser
from flask_login import LoginManager, login_required, logout_user, current_user, login_user
from pages import pages

app = Flask(__name__)
app.register_blueprint(pages)
urlconf = 'config/config.ini'
config = ConfigParser()
config.read(urlconf)
secret_key = config['flask']['secret_key']
app.secret_key = secret_key
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    try:
        user_type, id_ = user_id.split('_')
        user = mypackage.model.User.get_user_by_id(id_, user_type)
        return user
    except Exception as e:
        print(e)
        return None


# @app.route("/")
# def Main():
#     return render_template('index.html', context="/")


@app.route("/templates/menu.html")
def Menu():
    return render_template('menu.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
        user_type = request.form['user_type']
        user = mypackage.model.User.get_user(login, password, user_type)
        if user:
            login_user(user)
            return redirect(url_for('pages.Main'))
        flash('Invalid username or password')
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('pages.Main'))


@app.route("/teacher")
def Teacher():
    return render_template('teacher/teacher.html', context="/teacher")


@app.route("/teacher/students", methods=['POST'])
def List_of_students():  #сделать через 1 запрос
    fio = request.form.get('fio')
    result = mypackage.db_utils.get_class_id_by_teacher_name(fio.split())
    if result == 404:
        return 'Преподавателя с таким фио не существует, либо у него нет класса!', 404
    else:
        result = mypackage.db_utils.get_class_list_by_classid(result[0])
    return result


def teacher_required(f):
    def decorated_function(*args, **kwargs):
        if current_user.user_type != 'teacher':
            return redirect(url_for('Main'))
        return f(*args, **kwargs)
    return decorated_function


@app.route("/profile/teacher")
@login_required
@teacher_required
def Teacher_profile():
    id_ = current_user.id.split('_')[1]
    fio = mypackage.db_utils.get_teacher_fio(id_)
    return render_template("teacher/teacher-profile.html", fio=fio)


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
    for i in range(len(dicts_data)):
        dicts_data[i]['date'] = dicts_data[i]['date'].isoformat()
    json_data = json.dumps(dicts_data)
    return json_data

@login_required
@teacher_required
@app.route("/profile/teacher/add-grade", methods=['POST'])
def Add_grade():
    json_data = request.get_json()
    if current_user.user_type=='teacher':
        teacherid = current_user.id.split('_')[1]
        teacherfio = mypackage.db_utils.get_teacher_fio(teacherid)
        error = mypackage.db_utils.Add_grade(json_data, teacherid, teacherfio)
        if error:
            json_res = [{'error': str(error)}]
        else:
            result = mypackage.db_utils.get_grades_by_teacher(teacherfio)
            fields = ['name', 'classname', 'subject', 'grade', 'date']
            dicts_data = [dict(zip(fields, values)) for values in result]
            for i in range(len(dicts_data)):
                dicts_data[i]['date'] = dicts_data[i]['date'].isoformat()
            dicts_data.append({'error': 0})
            json_res = dicts_data
        return json.dumps(json_res)
    return "Нет доступа", 404

if __name__ == "__main__":
    app.run()
